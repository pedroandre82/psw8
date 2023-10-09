from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpRequest, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login


# Create your views here.

def cadastro(request: HttpRequest):
    if request.method == "GET":
        return render(request, template_name="usuarios/cadastro.html")
    elif request.method == "POST":
        nome: str = request.POST.get("primeiro_nome", "")
        sobrenome: str = request.POST.get("sobrenome", "")
        cpf: str = request.POST.get("cpf", "")
        email: str = request.POST.get("email", "")
        senha: str = request.POST.get("senha", "") 
        confirmar_senha = request.POST.get("confirmar_senha", "")

        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, "As senhas não são iguais")
            return redirect("usuarios:cadastro")
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, "Senha deve ter 6 caracteres pelo menos")
            return redirect("usuarios:cadastro")
        
        try:
            user = User.objects.create_user(
                first_name=nome,
                last_name=sobrenome,
                username=cpf,
                email=email,
                password=senha,
            )
        except:
            return redirect("usuarios:cadastro")

        messages.add_message(request, constants.SUCCESS, "Usuário cadastrado com sucesso")
        return redirect("usuarios:login")


def user_login(request: HttpRequest):
    if request.method == "GET":
        return render(request, template_name="usuarios/login.html")
    elif request.method == "POST":
        cpf = request.POST.get("cpf")
        senha = request.POST.get("senha")
        
        user = authenticate(username=cpf, password=senha)

        if not user:
            messages.add_message(request, constants.ERROR, "Usuário ou senha inválidos")
            return redirect("usuarios:login")

        login(request, user)

        if user.is_staff:
            return redirect("empresarial:gerenciar_clientes")
        else:
            return redirect("exames:gerenciar_pedidos")
