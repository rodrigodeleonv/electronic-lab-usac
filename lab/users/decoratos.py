# https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html
# admin:login es nombre de la url que indica que hay que autenticar con mas privilegios
# https://github.com/django/django/blob/stable/1.9.x/django/contrib/admin/views/decorators.py

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


# def administrador_requiered(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='users:login_permission'):
# 	"""Decorator for view. Check if logged user is admin"""
# 	actual_decorator = user_passes_test(
# 		lambda u: u.role == u.ADMIN,
# 		login_url=login_url,
#         redirect_field_name=redirect_field_name
# 	)
# 	if function:
# 		return actual_decorator(function)
# 	return actual_decorator



# def subadministrador_requiered(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='users:login_permission'):
# 	"""Decorator for view. Check if logged user is admin"""
# 	actual_decorator = user_passes_test(
# 		lambda u: u.role == u.ADMIN or u.role == u.SUB_ADMIN,
# 		login_url=login_url,
#         redirect_field_name=redirect_field_name
# 	)
# 	if function:
# 		return actual_decorator(function)
# 	return actual_decorator



# def distribuidor_requiered(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='users:login_permission'):
# 	actual_decorator = user_passes_test(
# 		lambda u: u.role == u.ADMIN or u.role == u.SUB_ADMIN or u.role == u.DISTRIBUIDOR,
# 		login_url=login_url,
#         redirect_field_name=redirect_field_name
# 	)
# 	if function:
# 		return actual_decorator(function)
# 	return actual_decorator


# def distribuidor_admin_requiered(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='users:login_permission'):
# 	actual_decorator = user_passes_test(
# 		lambda u: u.role == u.ADMIN or u.role == u.DISTRIBUIDOR,
# 		login_url=login_url,
#         redirect_field_name=redirect_field_name
# 	)
# 	if function:
# 		return actual_decorator(function)
# 	return actual_decorator


# def subdistribuidor_requiered(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='users:login_permission'):
# 	actual_decorator = user_passes_test(
# 		lambda u: u.role == u.ADMIN or u.role == u.SUB_ADMIN or u.role == u.DISTRIBUIDOR or u.role == u.SUB_DISTRIBUIDOR,
# 		login_url=login_url,
#         redirect_field_name=redirect_field_name
# 	)
# 	if function:
# 		return actual_decorator(function)
# 	return actual_decorator



# def piloto_requiered(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='users:login_permission'):
# 	actual_decorator = user_passes_test(
# 		lambda u: u.role == u.ADMIN or u.role == u.SUB_ADMIN or u.role == u.PILOTO,
# 		login_url=login_url,
#         redirect_field_name=redirect_field_name
# 	)
# 	if function:
# 		return actual_decorator(function)
# 	return actual_decorator

