from django.urls import path
from . import views

app_name = "exames"
urlpatterns = [
    path('', views.index, name="index"),
    path('solicitar/', views.solicitar, name="solicitar"),
    path('fechar_pedido/', views.fechar_pedido, name="fechar_pedido"),
    path('gerenciar_pedidos/', views.gerenciar_pedidos, name="gerenciar_pedidos"),
    path('gerenciar_exames/', views.gerenciar_exames, name="gerenciar_exames"),
    path('cancelar_pedido/<int:id_pedido>', views.cancelar_pedido, name="cancelar_pedido"),
    path('permitir_abrir_exame/<int:id_exame>', views.permitir_abrir_exame, name="permitir_abrir_exame"),
    path('solicitar_senha_exame/<int:id_exame>', views.solicitar_senha_exame, name="solicitar_senha_exame"),
    path('acesso_medico/<str:token>', views.acesso_medico, name="acesso_medico"),
    path('gerar_acesso_medico/', views.gerar_acesso_medico, name="gerar_acesso_medico"),
]
