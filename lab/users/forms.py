from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Distribuidora

# Another way to create user random password
# https://django-authtools.readthedocs.io/en/latest/how-to/invitation-email.html

class CustomUserCreationForm(UserCreationForm):

	class Meta:
		model = CustomUser
		fields = ('first_name', 'last_name', 'email')
		labels = {
			'first_name': 'Nombres',
			'email': 'Email'
		}


class CustomUserChangeForm(UserChangeForm):

	class Meta:
		model = CustomUser
		fields = ('email',)


class CustomUserForm(forms.ModelForm):

	class Meta(UserCreationForm.Meta):
		model = CustomUser
		fields = ('email', 'first_name', 'last_name')
		labels = {
			'first_name': 'Nombres',
			'email': 'Email'
		}


class UserDistribuidorPublicForm(UserCreationForm):

	class Meta:
		model = CustomUser
		fields = ('email', 'first_name', 'last_name')
		labels = {
			'first_name': _('Nombres del Propietario'),
			'last_name': _('Apellidos del propietario'),
			'email': 'Email'
		}


class DistribuidoraForm(forms.ModelForm):

	def clean_owner_dpi(self):
		data = self.cleaned_data['owner_dpi']
		if len(data) != 13:
			raise forms.ValidationError('La cantidad de digitos en el DPI es incorrecto', code='invalid')
		try:
			int(data)
		except:
			raise forms.ValidationError('DPI debe contener solo números [0-9]', code='invalid')
		return data

	def clean(self):
		super().clean()
		cash_payment = self.cleaned_data['cash_payment']
		monthly_payment = self.cleaned_data['monthly_payment']
		if cash_payment == False and monthly_payment == False:
			raise forms.ValidationError('Debe elegir al menos una forma de pago', code='invalid')

	
	class Meta:
		model = Distribuidora
		fields = [
			'name', 'address', 'phone_number', 'owner_name', 'owner_dpi',
			'com_ref1', 'com_ref1_phone', 'com_ref2', 'com_ref2_phone', 'com_ref3', 'com_ref3_phone',
			'bank_references', 'cash_payment', 'monthly_payment', 'website', 'description'
		]


class DistribuidoraPublicForm(DistribuidoraForm):

	class Meta(DistribuidoraForm.Meta):
		fields = [
			'owner_dpi', 'name', 'address', 'phone_number',
			'com_ref1', 'com_ref1_phone', 'com_ref2', 'com_ref2_phone', 'com_ref3', 'com_ref3_phone',
			'bank_references', 'cash_payment', 'monthly_payment', 'website', 'description'
		]
