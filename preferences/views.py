from django.shortcuts import render
import os
import json
from django.conf import settings
from django.contrib import messages
from .models import Currency

# Create your views here.


def preferences_view(request):
    user_preferences = Currency.objects.filter(user=request.user)[
        0] if Currency.objects.filter(user=request.user).exists() else None

    file = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        currency_data = []
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    if request.method == 'GET':
        return render(request, 'preferences/index.html',
                      {'currencies': currency_data,
                       'user_preferences': user_preferences})
    else:
        currency = request.POST['currency']
        if user_preferences is not None:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            Currency.objects.create(user=request.user, currency=currency)
            user_preferences['currency'] = currency
        messages.success(request, 'Changes saved')

        return render(request, 'preferences/index.html',
                      {'currencies': currency_data,
                       'user_preferences': user_preferences})


def settings_view(request):
    return render(request, 'preferences/settings.html')



