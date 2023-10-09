from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from secrets import token_urlsafe
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import resolve_url

# Create your models here.

class TiposExames(models.Model):

    class Meta:
        verbose_name = "Tipo de Exame"
        verbose_name_plural = "Tipos de Exame"

    TIPO_CHOICES = (
        ('I', 'Exame de imagem'),
        ('S', 'Exame de sangue'),
    )
    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    preco = models.FloatField()
    disponivel = models.BooleanField(default=True)
    horario_inicial = models.IntegerField()
    horario_final = models.IntegerField()

    def __str__(self):
        return self.nome
    

class SolicitacaoExame(models.Model):

    class Meta:
        verbose_name = "Solicitação de Exame"
        verbose_name_plural = "Solicitações de Exame"

    status_choices = (
        ('E', 'Em análise'),
        ('F', 'Finalizado'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    exame = models.ForeignKey(TiposExames, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=status_choices)
    resultado = models.FileField(upload_to='resultados', null=True, blank=True)
    requer_senha = models.BooleanField(default=False)
    senha = models.CharField(max_length=6, null=True, blank=True)


    def __str__(self):
        return f"{self.usuario} | {self.exame.nome}"
    
    def html_badge(self):
        if self.status == 'E':
            classes_css = 'bg-warning text-dark'
            texto = "Em análise"
        elif self.status == 'F':
            classes_css = 'bg-success'
            texto = "Finalizado"
        
        return mark_safe(f"<span class='badge bg-primary {classes_css}'>{texto}</span>")
    

class PedidosExames(models.Model):

    class Meta:
        verbose_name = "Pedido de Exame"
        verbose_name_plural = "Pedidos de Exame"

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    exames = models.ManyToManyField(SolicitacaoExame)
    agendado = models.BooleanField(default=True)
    data = models.DateField()

    def __str__(self):
        return f"{self.usuario} | {self.data}"


class AcessoMedico(models.Model):

    class Meta:
        verbose_name = "Acesso do Médico"
        verbose_name_plural = "Acessos do Médico"


    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    identificacao = models.CharField(max_length=50)
    tempo_de_acesso = models.IntegerField() # Em horas
    criado_em = models.DateTimeField()
    data_exames_iniciais = models.DateField()
    data_exames_finais = models.DateField()
    token = models.CharField(max_length=20)

    def __str__(self):
        return self.token
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = token_urlsafe(6)

        super(AcessoMedico, self).save(*args, **kwargs)

    @property
    def status(self):
        return "Expirado" if timezone.now() > (self.criado_em + timedelta(hours=self.tempo_de_acesso)) else 'Ativo'
    
    @property
    def url(self):
        return resolve_url("exames:acesso_medico", self.token)
