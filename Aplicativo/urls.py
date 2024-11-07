from django.urls import path,include
from Aplicativo.views import retornar_index
from .funcoes.eletivas import eletivas
from .funcoes.sobre import sobre
from .funcoes.tutoria import tutoria
from .funcoes.logout import logout_viwes

urlpatterns = [
    path('', retornar_index,name='index'),
    path('logout/',logout_viwes ,name='logout'),
    path('sobre/',sobre,name='sobre'),
    path('eletivas/', eletivas,name='eletivas'),
    # path('eletiva/<str:eletiva>',ver_eletiva,name='ver-eletiva'),
    path('tutoria/',tutoria,name='tutoria'),  

    
]
