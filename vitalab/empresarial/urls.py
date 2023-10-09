from django.urls import path, include
from . import views

app_name = "empresarial"
urlpatterns = [
    path('gerenciar_clientes/', views.gerenciar_clientes, name="gerenciar_clientes"),
    path('cliente/<int:id_cliente>', views.cliente, name="cliente"),
    path('exame_cliente/<int:id_exame>', views.exame_cliente, name="exame_cliente"),
    path('proxy_pdf/<int:id_exame>', views.proxy_pdf, name="proxy_pdf"),
    path('gerar_senha/<int:id_exame>', views.gerar_senha, name="gerar_senha"),
    path('alterar_dados_exame/<int:id_exame>', views.alterar_dados_exame, name="alterar_dados_exame"),
]
