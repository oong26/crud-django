from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/authentication/login")
def index(request):
    return render(request, 'expenses/index.html')

def create(request):
    return render(request, 'expenses/create.html')