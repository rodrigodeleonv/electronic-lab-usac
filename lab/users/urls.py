from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    # path(''),


    # path('login/permissions/', views.login_permissions, name='login_permission'),

    # path('profile/', views.profile, name='profile'),
    # path('profile/u_show/', views.users_show, name='users_show'),

    # path('<int:pk>/detail/', views.user_detail, name='user_detail'),
    # path('<int:pk>/detail/<str:random_pass>/new', views.user_detail, name='user_detail_pass'),
    # path('<int:pk>/detail/new', views.user_detail, name='user_detail_nopass'),
    # path('<int:pk>/modify/', views.user_modify, name='user_modify'),
    # path('<int:pk>/fdelete/', views.user_fdelete, name='user_fdelete'),

    # path('admin/create/', views.create_admin_user, name='create_admin_user'),		
    # path('create/sub-admin/', views.create_sub_admin_user, name='create_sub_admin_user'),

    # path('create/distribuidor/', views.create_distribuidor_user, name='create_distribuidor_user'),
    # path('create/distribuidor/<int:pk>/', views.create_distribuidor_user, name='create_distribuidor_user_pk'),
    # path('create/sub-distribuidor/', views.create_sub_distribuidor_user, name='create_sub_distribuidor_user'),
    # path('create/sub-distribuidor/<int:pk>/', views.create_sub_distribuidor_user, name='create_sub_distribuidor_user'),

    # path('create/piloto/', views.create_piloto, name='create_piloto'),

    # path('distribuidoras/approve/', views.distribuidora_approve, name='distribuidora_approve'),
    # path('distribuidoras/<int:pk>/approve/', views.distribuidora_approve, name='distribuidora_approve_validate'),
    # path('distribuidoras/approve/<int:pk>/details/', views.distribuidora_approve_redirect, name='distribuidora_approve_redirect'),
    # path('distribuidoras/show/', views.distribuidora_show, name='distribuidoras'),
    # path('distribuidoras/deleted/', views.distribuidora_deleted, name='distribuidoras_deleted'),
    # path('distribuidoras/<int:pk>/detail/', views.distribuidora_detail, name='distribuidora_detail'),
    # path('distribuidoras/<int:pk>/modify/', views.distribuidora_modify, name='distribuidora_modify'),
    # path('distribuidoras/<int:pk>/fdelete/', views.distribuidora_fdel, name='distribuidora_fdel'),

    # # Test
    # path('create_user/', views.create_user, name='create_user'),
]

# translation_urls = ([
#     path('register/company/', views.distribuidora_register, name='distribuidora_register'),
#     path('register/company/succesful/', views.distribuidora_register_redirect, name='distribuidora_register_redirect'),
# ], 'users')
