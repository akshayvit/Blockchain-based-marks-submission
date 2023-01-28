from django.urls import path
from . import views


urlpatterns = [
    path('members/',views.showform,name='members_info'),
    path('adddata/',views.adddata,name='members_info_add'),
    path('delete/<int:roll>',views.deletedata,name='members_info_delete'),
    path('update/<int:roll>',views.updatedata,name='members_info_update'),
    
]
