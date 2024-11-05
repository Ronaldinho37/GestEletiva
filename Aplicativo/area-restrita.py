from django.urls import path
from Aplicativo.views import *

urlpatterns = [
    path('update_or_delete/<str:u_or_d>/<str:user_a_ser_atualizado_arg>',update_or_delete,name="update_or_delete"),
    path('',login_viwes ,name='login'),
 #   path('sobre/',sobre,name='sobre'),
    path('logout/',logout_viwes ,name='logout'),
   # path('eletivas/', eletivas,name='eletivas'),
    path('add-eletiva/', add_eletivas,name='add-eletiva'),
    path('add/<str:tipo_de_user>', add_professor,name='add'),
  #  path('eletiva/<str:eletiva>',ver_eletiva,name='ver-eletiva'),
    path('update/<str:user_a_ser_atualizado_arg>/<int:id>',update_com_id,name='update_com_id'),
   # path('add-aluno/',add_aluno,name='add-aluno'),
    path('add-admin/',add_admin,name='add-admin'),
 #   path('tutoria/',tutoria,name='tutoria'),
    path('definir-paginas/',definir_paginas_utilizaveis,name='definir-paginas'),
    path('editar_aviso/<int:id>',editar_aviso,name='editar_aviso'),
    path('editar_oferecimento/<int:id>',editar_oferecimento,name='editar_oferecimento'),
    path('deletar/<str:user_a_ser_atualizado_arg>/<str:id>',deletar_com_ids,name='deletar_com_ids'),
    path('add_oferecimento',add_OqueTemosaOferecer,name='add_oferecimento'),
    path('carrossel/adicionar',add_professor_carrossel,name='add_professor_carrossel'),
    path('carrossel/atualizar/<int:id>',update_carrossel,name='atualizar_carrossel'),
    path('carrossel/deletar/<int:id>',deletar_carrossel,name='deletar_carrossel'),

    
]