from django.shortcuts import render
import os
import json
from django.conf import settings
from django.contrib import messages
from .models import Currency

# Create your views here.


def preferences_view(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    exists = Currency.objects.filter(user=request.user).exists()
    user_currency = None

    if exists:
        user_currency = Currency.objects.get(user=request.user)

    if request.method == 'GET':
        return render(request, 'preferences/index.html',
                      {'currencies': currency_data,
                       'user_currency': user_currency})
    else:
        currency = request.POST['currency']
        if exists:
            user_currency.currency = currency
            user_currency.save()
        else:
            Currency.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved')
        return render(request, 'preferences/index.html',
                      {'currencies': currency_data,
                       'user_currency': user_currency})





