from django.shortcuts import render, get_object_or_404, redirect
# from django.urls import reverse
# from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
# from .decoratos import (
#     administrador_requiered, subadministrador_requiered, distribuidor_requiered, distribuidor_admin_requiered
# )
from users.forms import UserCreationForm
# from users.models import CustomUser, Distribuidora #, Profile
from django.db.models import Q
# from django.core.mail import send_mail
# from django.template import loader
# from django.conf import settings
# from datetime import date


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
