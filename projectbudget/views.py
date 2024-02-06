from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.


# ---->>>>>>>>>> PROJECT BUDGET - PAGE VIEW <<<<<<<<<<<<----#

@login_required(login_url='/authentication/login')
def project_budget_view(request):
    return render(request, 'projectbudget/index.html')
