from django.shortcuts import render

from web.forms import RegistrationForm


def main_view(request):
    return render(request, 'web/main.html')


def registration_view(request):
    form = RegistrationForm()
    return render(request, 'web/registration.html', {'form': form})
