from django.shortcuts import render, get_object_or_404, redirect
# from django.urls import reverse
# from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .decoratos import (
	administrador_requiered, subadministrador_requiered, distribuidor_requiered, distribuidor_admin_requiered
)
from .forms import CustomUserCreationForm, CustomUserForm, DistribuidoraForm
from .models import CustomUser, Distribuidora #, Profile
from django.db.models import Q
from boletos.models import DistribuidoraRuta
from django.core.mail import send_mail
from django.template import loader
from django.conf import settings
from datetime import date



#
#  Common functions
#

def is_administrator(user_instance):
	if user_instance.role == CustomUser.ADMIN:
		return True
	else:
		return False

def is_distribuidor(user_instance):
	if user_instance.role == CustomUser.DISTRIBUIDOR:
		return True
	else:
		return False

def random_password(length=None):
	if length and length >= 10:
		return CustomUser.objects.make_random_password(length=length)
	else:
		return CustomUser.objects.make_random_password()
	#return 'supervalue10'


#
# --------------------------------
#



@login_required
def login_permissions(request):
	"""Show message no enough permition to access"""
	context = {
		# HTTP_REFERER = request.META.get('HTTP_REFERER', None),
		# 'QUERY_STRING': request.META['QUERY_STRING'],
	}
	return render(request, 'registration/login_perms.html', context)


@login_required
def profile(request):
	context = {
		'cuser': CustomUser.objects.select_related('profile').get(pk=request.user.id)
	}
	return render(request, 'users/profile.html', context)


@login_required
@distribuidor_requiered
def users_show(request):
	"""Show registered Users"""
	search = request.GET.get('search', None)
	current_user = request.user
	if current_user.role <= CustomUser.SUB_ADMIN:
		if search:
			cusers = CustomUser.objects.select_related('profile').filter(
				Q(first_name__icontains=search)|Q(last_name__icontains=search)|
				Q(email__icontains=search)|Q(profile__distribuidora__name__icontains=search),
				deleted=False
			).order_by('role', 'profile__distribuidora')
		else:
			cusers = CustomUser.objects.select_related('profile').filter(deleted=False).order_by('role', 'profile__distribuidora')
	elif current_user.role == CustomUser.DISTRIBUIDOR:
		if search:
			cusers = CustomUser.objects.select_related('profile').filter(
				Q(first_name__icontains=search)|Q(last_name__icontains=search)|
				Q(email__icontains=search)|Q(profile__distribuidora__name__icontains=search),
				deleted=False, profile__distribuidora=current_user.profile.distribuidora
			).order_by('role', 'profile__distribuidora')
		else:
			cusers = CustomUser.objects.select_related('profile').filter(
				deleted=False, profile__distribuidora=current_user.profile.distribuidora
			).order_by('role', 'profile__distribuidora')
	context = {
		'cusers': cusers,
	}
	return render(request, 'users/users.html', context)



@login_required
@distribuidor_requiered
def user_detail(request, pk, random_pass=None):
	current_user = request.user
	if current_user.role <= CustomUser.SUB_ADMIN:
		cuser = get_object_or_404(CustomUser.objects.select_related(), pk=pk)
	elif current_user.role == CustomUser.DISTRIBUIDOR:
		cuser = get_object_or_404(CustomUser.objects.select_related(), pk=pk, profile__distribuidora=current_user.profile.distribuidora)
	else:
		cuser = None
		random_pass = None

	context = {
		'cuser': cuser,
		'random_pass': random_pass,
	}
	return render(request, 'users/user_detail.html', context)



@login_required
@distribuidor_admin_requiered
def user_modify(request, pk):
	current_user = request.user
	if current_user.role == CustomUser.ADMIN:
		cuser = get_object_or_404(CustomUser, pk=pk)
	elif current_user.role == CustomUser.DISTRIBUIDOR:
		cuser = get_object_or_404(CustomUser, pk=pk, profile__distribuidora=current_user.profile.distribuidora)

	if request.method == "POST":
		form_user = CustomUserForm(request.POST, instance=cuser)
		if form_user.is_valid():
			form_user.save()
			return redirect('users:user_detail', pk=pk)
	else:
		form_user = CustomUserForm(instance=cuser)
	context = {
		'form_user': form_user,
		'cuser': cuser,
	}
	return render(request, 'users/user_modify.html', context)



@login_required
@distribuidor_admin_requiered
def user_fdelete(request, pk):
	current_user = request.user
	if current_user.role == CustomUser.ADMIN:
		cuser = get_object_or_404(CustomUser.objects.select_related(), pk=pk)
	else:
		cuser = get_object_or_404(CustomUser.objects.select_related(), pk=pk, profile__distribuidora=current_user.profile.distribuidora)

	if cuser == current_user:
		return render(request, 'users/user_fdel.html', {'cuser': cuser, 'prohibited': True})

	if request.method == 'POST':
		delete = request.POST.get('delete', None)
		if delete == 'True':
			cuser.deleted = True
			cuser.is_active = False
			cuser.save(update_fields=['deleted', 'is_active'])
		elif delete == 'False':
			cuser.deleted = False
			cuser.is_active = True
			cuser.save(update_fields=['deleted', 'is_active'])
		return redirect('users:user_fdelete', pk=pk)

	context = {
		'cuser': cuser,
	}
	return render(request, 'users/user_fdel.html', context)



@login_required
@administrador_requiered
def create_admin_user(request):
	"""Create a new user"""
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			cuser = form.save(commit=False)
			cuser.role = CustomUser.ADMIN
			cuser.save()
			return redirect('users:user_detail_nopass', pk=cuser.pk)
	else:
		form = CustomUserCreationForm()

	context = {
		'form': form,
		'user_role': 'Administrador'
	}
	return render(request, 'users/user_create.html', context)



@login_required
@administrador_requiered
def create_sub_admin_user(request):
	if request.method == 'POST':
		form = CustomUserForm(request.POST)
		if form.is_valid():
			random_pass = random_password()
			cuser = form.save(commit=False)
			cuser.set_password(random_pass)
			cuser.role = CustomUser.SUB_ADMIN
			cuser.save()
			return redirect('users:user_detail_pass', pk=cuser.pk, random_pass=random_pass)
	else:
		form = CustomUserForm()

	context = {
		'form': form,
		'user_role': 'Sub-administrador'
	}
	return render(request, 'users/user_create.html', context)



@login_required
@administrador_requiered
def create_distribuidor_user(request, pk=None):
	"""Create a new user distribuidor with Distribuidora associate via Profile"""
	search = request.GET.get('search', None)	
	if pk == None:
		step = 'step1'
		if search:
			distribuidoras = Distribuidora.objects.filter(name__icontains=search).order_by('name')
		else:
			distribuidoras = Distribuidora.objects.order_by('name')
	else:
		step = 'step2'
		distribuidoras = None
		distribuidora = get_object_or_404(Distribuidora, pk=pk)

	if request.method == 'POST' and pk != None:
		form = CustomUserForm(request.POST)
		with transaction.atomic():
			if form.is_valid():
				random_pass = random_password()
				cuser = form.save(commit=False)
				cuser.set_password(random_pass)
				cuser.role = CustomUser.DISTRIBUIDOR
				cuser.save() # To create Profile Model then update Profile				
				cuser.profile.distribuidora = distribuidora
				cuser.save()
				return redirect('users:user_detail_pass', pk=cuser.pk, random_pass=random_pass)
	else:
		form = CustomUserForm()

	context = {
		'form': form,
		'distribuidoras': distribuidoras,
		'step': step,
	}
	return render(request, 'users/user_create_distribuidor.html', context)



@login_required
@distribuidor_requiered
def create_sub_distribuidor_user(request, pk=None):
	"""Create a new user Sub-distribuidor"""
	search = request.GET.get('search', None)
	current_user = request.user
	distribuidoras = None
	distribuidora = None
	step = None

	if is_administrator(current_user):
		if pk == None:
			step = 'step1'
			if search:
				distribuidoras = Distribuidora.objects.filter(deleted=False, name__icontains=search).order_by('name')
			else:
				distribuidoras = Distribuidora.objects.filter(deleted=False).order_by('name')
		else:
			step = 'step2'
			distribuidora = get_object_or_404(Distribuidora, pk=pk, deleted=False)
	elif is_distribuidor(current_user):
		distribuidora = current_user.profile.distribuidora
	
	# form = create_sub_distribuidor(distribuidora)
	if request.method == 'POST' and distribuidora:
		form = CustomUserForm(request.POST)
		with transaction.atomic():
			if form.is_valid():
				random_pass = random_password()
				cuser = form.save(commit=False)
				cuser.set_password(random_pass)
				cuser.role = CustomUser.SUB_DISTRIBUIDOR
				cuser.save()				
				cuser.profile.distribuidora = distribuidora
				cuser.save()
				return redirect('users:user_detail_pass', pk=cuser.pk, random_pass=random_pass)	
	else:
		form = CustomUserForm()

	context = {
		'form': form,
		'distribuidoras': distribuidoras,
		'step': step,
	}
	return render(request, 'users/user_create_sub_dist.html', context)



@login_required
@administrador_requiered
def create_piloto(request):
	if request.method == 'POST':
		form = CustomUserForm(request.POST)
		if form.is_valid():
			random_pass = random_password()
			cuser = form.save(commit=False)
			cuser.set_password(random_pass)
			cuser.role = CustomUser.PILOTO
			cuser.save()
			return redirect('users:user_detail_pass', pk=cuser.pk, random_pass=random_pass)
	else:
		form = CustomUserForm()

	context = {
		'form': form,
		'user_role': 'Piloto'
	}
	return render(request, 'users/user_create.html', context)



@login_required
@subadministrador_requiered
def distribuidora_approve(request, pk=None):
	distribuidoras = None
	distribuidora = None
	owner_user = None

	if pk == None:
		distribuidoras = Distribuidora.objects.filter(deleted=False, approved=None)
	else:		
		validate = request.POST.get('validate', None)
		current_user = request.user
		distribuidora = get_object_or_404(Distribuidora, pk=pk, deleted=False, approved=None)
		cusers = CustomUser.objects.filter(profile__distribuidora=distribuidora, role=CustomUser.DISTRIBUIDOR).order_by('id')[:1]
		if len(cusers) > 0:
			owner_user = cusers[0]	
		## -------------------------------------
		# html_message = loader.render_to_string(
		# 	'email/approve_registration.html',
		# 	{
		# 		'full_name': owner_user.get_full_name(),
		# 		'distribuidora':  distribuidora.name,
		# 		'username': owner_user.get_username(),
		# 	}
		# )
		# send_mail(
		# 	subject='Registro en PacificSurfgt - Aprobado',
		# 	message='Su registro ha sido aprobado en pacificsurfgt.com',
		# 	from_email=settings.EMAIL_HOST_USER,
		# 	recipient_list=[owner_user.email],
		# 	fail_silently=False,
		# 	html_message=html_message
		# )
		# print(owner_user.get_full_name(), distribuidora.name, owner_user.get_username(), owner_user.email)
		## -------------------------------------
		if validate == 'approved':
			distribuidora.approved = True
			distribuidora.approved_by = current_user
			distribuidora.approved_date = date.today()
			distribuidora.save(update_fields=['approved','approved_by','approved_date'])
			# ---
			owner_user.deleted = False
			owner_user.is_active = True
			owner_user.save(update_fields=['deleted','is_active'])
			# ---			
			html_message = loader.render_to_string(
				'email/approve_registration.html',
				{
					'full_name': owner_user.get_full_name(),
					'distribuidora':  distribuidora.name,
					'username': owner_user.get_username(),
				}
			)
			send_mail(
				subject='Registro en PacificSurfgt - Aprobado',
				message='Su registro ha sido aprobado en pacificsurfgt.com',
				from_email=settings.EMAIL_HOST_USER,
				recipient_list=[owner_user.email],
				fail_silently=True,
				html_message=html_message
			)
			return redirect('users:distribuidora_approve_redirect', pk=distribuidora.pk)
		elif validate == 'rejected':
			html_message = loader.render_to_string(
				'email/reject_registration.html',
				{
					'full_name': owner_user.get_full_name()
				}
			)
			send_mail(
				subject='Registro en PacificSurfgt',
				message='Su registro no ha sido aprobado en pacificsurfgt.com',
				from_email=settings.EMAIL_HOST_USER,
				recipient_list=[owner_user.email],
				fail_silently=True,
				html_message=html_message
			)
			return redirect('users:distribuidora_approve_redirect', pk=distribuidora.pk)
		else:
			pass

	context = {
		'distribuidoras': distribuidoras,
		'distribuidora': distribuidora,
		'owner_user': owner_user,
		'pk': pk,
	}
	return render(request, 'users/distribuidora_approve.html', context)



@login_required
@subadministrador_requiered
def distribuidora_approve_redirect(request, pk):
	# approved = request.GET.get('approved', None)
	distribuidora = get_object_or_404(Distribuidora, pk=pk)
	cusers = CustomUser.objects.filter(profile__distribuidora=distribuidora, role=CustomUser.DISTRIBUIDOR).order_by('id')[:1]
	if len(cusers) > 0:
		owner_user = cusers[0]
	else:
		owner_user = None
	context = {
		'distribuidora': distribuidora,
		'owner_user': owner_user,
	}
	return render(request, 'users/distribuidora_approve_redirect.html', context)


@login_required
@subadministrador_requiered
def distribuidora_show(request):
	search = request.GET.get('search', None)
	if search:
		distribuidoras = Distribuidora.objects.filter(
			Q(name__icontains=search)| Q(address__icontains=search), deleted=False
		)
	else:
		distribuidoras = Distribuidora.objects.filter(deleted=False)
	context = {
		'distribuidoras': distribuidoras,
	}
	return render(request, 'users/distribuidora.html', context)



@login_required
@subadministrador_requiered
def distribuidora_deleted(request):
	search = request.GET.get('search', None)
	if search:
		distribuidoras = Distribuidora.objects.filter(
			Q(name__icontains=search)| Q(address__icontains=search), deleted=True
		)
	else:
		distribuidoras = Distribuidora.objects.filter(deleted=True)
	context = {
		'distribuidoras': distribuidoras,
	}
	return render(request, 'users/distribuidora_deleted.html', context)



@login_required
@subadministrador_requiered
def distribuidora_detail(request, pk):
	distribuidora = get_object_or_404(Distribuidora, pk=pk, deleted=False)
	cusers = CustomUser.objects.filter(profile__distribuidora=distribuidora).order_by('role', 'id')
	
	context = {
		'distribuidora': distribuidora,
		'cusers': cusers,
	}
	return render(request, 'users/distribuidora_detail.html', context)



@login_required
@administrador_requiered
def distribuidora_modify(request, pk):
	distribuidora = get_object_or_404(Distribuidora, pk=pk, deleted=False)
	if request.method == 'POST':
		form = DistribuidoraForm(request.POST, instance=distribuidora)
		if form.is_valid():
			form.save()
			return redirect('users:distribuidora_detail', pk=pk)
	else:
		form = DistribuidoraForm(instance=distribuidora)
	context = {
		'form': form,
	}
	return render(request, 'users/distribuidora_modif.html', context)	




@login_required
@administrador_requiered
def distribuidora_fdel(request, pk):
	"""
	Fake delete Distribuidora:
		1. Mark Distribuidora as deleted
		2. Mark DistribuidoraRuta ManytoMany relationship as deleted (if deleted exists there)
		3. Mark Distribuidores and Sub-distribuidores as deleted and is_active=False
	"""

	#
	# Falta analizar que pasará con sus Deudas Pendientes
	#

	distribuidora = get_object_or_404(Distribuidora, pk=pk)
	drs = DistribuidoraRuta.objects.filter(distribuidora=distribuidora)
	cusers = CustomUser.objects.select_related().filter(profile__distribuidora=distribuidora)
	if request.method == 'POST':
		distribuidora.deleted = True
		distribuidora.save(update_fields=['deleted'])
		for dr in drs:
			if dr.deleted == False:
				dr.deleted = True
				dr.save(update_fields=['deleted'])
		for u in cusers:
			u.deleted = True
			u.is_active = False
			u.save(update_fields=['deleted', 'is_active'])
	else:
		pass
	
	# #### Reactivate for test only ------------------------------------------------------------------
	# distribuidora.deleted = False
	# distribuidora.save(update_fields=['deleted'])
	# for dr in drs:
	# 	dr.deleted = False
	# 	dr.save(update_fields=['deleted'])
	# for u in cusers:
	# 	u.deleted = False
	# 	u.is_active = True
	# 	u.save(update_fields=['deleted', 'is_active'])
	# ### end debug -----------------------------------------------------------------------------------

	context = {
		'distribuidora': distribuidora,
		'drs': drs,
		'cusers': cusers,
	}
	return render(request, 'users/distribuidora_fdel.html', context)	



def distribuidora_register(request):
	""" 
	Public register for Empresas Distribuidoras
	"""
	from users.forms import DistribuidoraPublicForm, UserDistribuidorPublicForm
	if request.method == 'POST':
		distribuidora_form = DistribuidoraPublicForm(request.POST)
		user_distribuidor_form = UserDistribuidorPublicForm(request.POST)
		if distribuidora_form.is_valid():
			distribuidora = distribuidora_form.save(commit=False)
			distribuidora.owner_name = '{} {}'.format(request.POST.get('first_name'), request.POST.get('last_name'))
			distribuidora.save()
			with transaction.atomic():
				if user_distribuidor_form.is_valid():
					cuser = user_distribuidor_form.save(commit=False)
					cuser.role = CustomUser.DISTRIBUIDOR
					cuser.deleted = True
					cuser.is_active = False
					cuser.save()
					cuser.profile.distribuidora = distribuidora
					cuser.save()
					print('Empresa: {}\t Usuario: {}'.format(distribuidora, cuser.get_full_name()))
					return redirect('users_trans:distribuidora_register_redirect')
			## if not return redirect
			distribuidora.delete()
	else:
		distribuidora_form = DistribuidoraPublicForm()
		user_distribuidor_form = UserDistribuidorPublicForm()
	context = {
		'distribuidora_form': distribuidora_form,
		'user_distribuidor_form': user_distribuidor_form
	}
	return render(request, 'users/distribuidora_register.html', context)


def distribuidora_register_redirect(request):
	return render(request, 'users/distribuidora_reg_red.html', {})










def create_user(request):
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			print('Usuario guardardo correctamente.')
		else:
			print('Error, no se ha guardado el usuario.')

	# users = CustomUser.objects.select_related('profile')
	# for some_user in users:
	# 	print('{}\t\t{}'.format(some_user, some_user.profile.distribuidor))

	# users = CustomUser.objects.select_related('profile').filter(is_staff=False)
	# for u in users:
	# 	print('{}\t\t\t{}'.format(u.email, u.profile.distribuidor))

	# users = CustomUser.objects.select_related('profile').filter(~Q(profile__distribuidor=None))
	# for u in users:
	# 	print(u)

	# profile_users = Profile.objects.filter(customuser__is_staff=False).select_related('customuser')
	# for u in profile_users:
	# 	print(u)

	context = {
		'form': CustomUserCreationForm,
		'user_role': '',
	}
	return render(request, 'users/user_create.html', context)
