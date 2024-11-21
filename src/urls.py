from django.urls import path
from . import landing, views, example, client


urlpatterns = [
    # region LANDING PAGE ==========================================================================================
    path('', landing.login_user, name='login_user'),
    path('signup/', landing.signup, name='signup'),
    path('home/', landing.home, name='home'),
    path('logout/',landing.logout_user, name='logout'),
    
    path('refundpolicy/',landing.refundpolicy, name='refundpolicy'),
    path('termsandcondition/',landing.termsandcondition, name='termsandcondition'),
    path('privacypolicy/',landing.privacypolicy, name='privacypolicy'),
    path('contactus/',landing.contactus, name='contactus'),
    path('deliverymethod/',landing.deliverymethod, name='deliverymethod'),
    path('productlisting/',landing.productlisting, name='productlisting'),

    path('profile/',landing.profile, name='profile'),
    path('profile_setting/',landing.profile_setting, name='profile_setting'),

    # region ADMIN =================================================================================================
    path('adminhome/', views.adminhome, name='adminhome'),
    path('task/<int:pk>/', views.task_detail_view, name='task'),
    path('all-task-detail/<int:pk>/', views.all_task_detail_view, name='all-task-detail'),
    
    path('clienthome/', client.clienthome, name='clienthome'),
    path('client_profile/', client.client_profile, name='client_profile'),
    path('client_profile_setting/', client.client_profile_setting, name='client_profile_setting'),
    
    path('update-task-all/<int:pk>/', client.update_task_all, name='update-task-all'),
    path('update-task/<int:pk>/', client.update_task, name='update-task'),
    path('all-task/', client.all_task_list, name='all-task'),
    
    path('create-task/', client.create_task, name='create-task'),


    # region EXAMPLE ===============================================================================================
    path('table/',example.table, name='table'),
    path('graph/',example.graph, name='graph'),
    path('graph/bar/',example.graph, name='bargraph'),
    path('graph/pie/',example.graph, name='piegraph'),
    path('input/',example.input, name='input'),
    path('icon_list/',example.icon_list, name='icon_list'),
    path('button/',example.button, name='button'),
    path('card/',example.card, name='card'),
    path('layout/',example.layout, name='layout'),
    path('modal/',example.modal, name='modal'),
    path('page/',example.page, name='page'),
    path('animation/',example.animation, name='animation'),

    # WEBSITE SETTING
    path('app_setting/',landing.app_setting, name='app_setting'),
    path('page_creator/',example.page_creator, name='page_creator'),
    
]