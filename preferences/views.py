from django.shortcuts import render
import os
import json
from django.conf import settings
from django.contrib import messages
from .models import Currency

# Create your views here.


def preferences_view(request):
    user_preferences = Currency.objects.filter(owner=request.user).first()

    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        currency_data = [{'name': k, 'value': v} for k, v in data.items()]

    if request.method == 'GET':
        return render(request, 'preferences/index.html',
                      {'currencies': currency_data, 'user_preferences': user_preferences})

    elif request.method == 'POST':
        currency = request.POST.get('currency')

        if user_preferences is not None:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            Currency.objects.create(owner=request.user, currency=currency)

        messages.success(request, 'Changes saved')

    return render(request, 'preferences/index.html',
                  {'currencies': currency_data, 'user_preferences': user_preferences})


def settings_view(request):
    return render(request, 'preferences/settings.html')

# return redirect('preferences')  # Redirect after a successful POST
