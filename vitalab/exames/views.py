from django.shortcuts import render, redirect, resolve_url
from django.http import HttpRequest, HttpResponse
from .models import TiposExames, PedidosExames, SolicitacaoExame, AcessoMedico
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants


def index(request: HttpRequest):
    return HttpResponse("Página de exames")

@login_required
def solicitar(request: HttpRequest):
    tipos_exames = TiposExames.objects.all()
    if request.method == "GET":
        return render(
           request=request,
           template_name="exames/solicitar.html",
           context={"tipos_exames": tipos_exames}
        )
    elif request.method == "POST":
        id_exames = request.POST.getlist("exames_escolhidos")
        exames_solicitados = tipos_exames.filter(id__in=id_exames)

        preco_total = 0.0
        for exame in exames_solicitados:
            preco_total += exame.preco if exame.disponivel else 0

        return render(
           request=request,
           template_name="exames/solicitar.html",
           context={"tipos_exames": tipos_exames,
                    "exames_solicitados": exames_solicitados,
                    "preco_total": preco_total,
                    }
        )

@login_required
def fechar_pedido(request: HttpRequest):
    # if request.method == "GET":
    #     return
    
    id_exames = request.POST.getlist('exames')
    exames = TiposExames.objects.filter(id__in=id_exames)

    pedido = PedidosExames(
        usuario=request.user,
        data=datetime.now(),
    )
    pedido.save()

    for exame in exames:
        solicitacao = SolicitacaoExame(
            usuario=request.user,
            exame=exame,
            status="E",
        )
        solicitacao.save()
        pedido.exames.add(solicitacao)

    pedido.save()

    messages.add_message(request, constants.SUCCESS, 'Pedido de exame concluído com sucesso')
    return redirect("exames:gerenciar_pedidos")


@login_required
def gerenciar_pedidos(request: HttpRequest):
    pedidos = PedidosExames.objects.filter(usuario=request.user)
    return render(
        request=request,
        template_name="exames/gerenciar_pedidos.html",
        context={"pedidos": pedidos}
    )


@login_required
def cancelar_pedido(request: HttpRequest, id_pedido: int):
    pedido = PedidosExames.objects.get(id=id_pedido)
    
    if pedido.usuario != request.user:
        messages.add_message(request, constants.ERROR, 'Esse pedido não é seu')
        return redirect("exame:gerenciar_pedidos")
    
    pedido.agendado = False
    pedido.save()

    messages.add_message(request, constants.SUCCESS, 'Pedido excluído com sucesso')
    return redirect("exames:gerenciar_pedidos")


@login_required
def gerenciar_exames(request: HttpRequest):
    exames = SolicitacaoExame.objects.filter(usuario=request.user)
    exames_sangue = [exame for exame in exames if exame.exame.tipo == "S"]
    exames_imagem = [exame for exame in exames if exame.exame.tipo == "I"]

    return render(
        request=request,
        template_name="exames/gerenciar_exames.html",
        context={"exames_sangue": exames_sangue,
                 "exames_imagem": exames_imagem,
                 },
    )


@login_required
def permitir_abrir_exame(request: HttpRequest, id_exame):
    exame = SolicitacaoExame.objects.get(id=id_exame)
    #TODO: validar se o exame é do usuário
    if not exame.requer_senha:
        #TODO: verificar se o pdf existe
        return redirect(exame.resultado.url)
    else:
        return redirect(resolve_url("exames:solicitar_senha_exame", exame.id))
        # return redirect(f'/exames/solicitar_senha_exame/{exame.id}')


@login_required
def solicitar_senha_exame(request, id_exame):
    exame = SolicitacaoExame.objects.get(id=id_exame)
    if request.method == "GET":
        return render(request, 'exames/solicitar_senha_exame.html', {'exame': exame})
    elif request.method == "POST":
        senha = request.POST.get("senha")
        #TODO: validar se o exame é do usuário
        if senha == exame.senha:
            return redirect(exame.resultado.url)
        else:
            messages.add_message(request, constants.ERROR, 'Senha inválida')
            return redirect('exames:solicitar_senha_exame', exame.id)


def acesso_medico(request: HttpRequest, token: str):
    acesso = AcessoMedico.objects.get(token=token)

    if acesso.status == 'Expirado':
        messages.add_message(request, constants.WARNING, 'Esse link já se expirou!')
        return redirect('usuarios:login')

    pedidos = (
        PedidosExames.objects
        .filter(data__gte=acesso.data_exames_iniciais)
        .filter(data__lte=acesso.data_exames_finais)
        .filter(usuario=acesso.usuario)
    )
    
    return render(
        request=request,
        template_name="exames/acesso_medico.html",
        context={"pedidos": pedidos}
    )


@login_required
def gerar_acesso_medico(request):
    if request.method == "GET":
        acessos_medicos = AcessoMedico.objects.filter(usuario=request.user)
        return render(request, 
                      'exames/gerar_acesso_medico.html', 
                      {'acessos_medicos': acessos_medicos},
                      )
    
    elif request.method == "POST":
        identificacao = request.POST.get('identificacao')
        tempo_de_acesso = request.POST.get('tempo_de_acesso')
        data_exame_inicial = request.POST.get("data_exame_inicial")
        data_exame_final = request.POST.get("data_exame_final")

        acesso_medico = AcessoMedico(
            usuario = request.user,
            identificacao = identificacao,
            tempo_de_acesso = tempo_de_acesso,
            data_exames_iniciais = data_exame_inicial,
            data_exames_finais = data_exame_final,
            criado_em = datetime.now()
        )

        acesso_medico.save()

        messages.add_message(request, constants.SUCCESS, 'Acesso gerado com sucesso')
        return redirect('exames:gerar_acesso_medico')

