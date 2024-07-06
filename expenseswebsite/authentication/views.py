from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import auth

# Create your views here.
class RegisterView(View):
    context = {
        'app_name': settings.APP_NAME,
        'title': 'Register'
    }

    def get(self, request):
        return render(request, 'authentication/register.html', self.context)

    def post(self, request):
        self.context['fieldValues'] = request.POST

        # GET USER DATA
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # VALIDATE
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 8:
                    messages.warning(request, 'Password must have a minimum of 8 characters')
                    return render(request, 'authentication/register.html', self.context)

                # Store a user account
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                # user.is_active = False
                user.save()
                del self.context['fieldValues']

                # Send confirmation email
                # email_subject = "Activate your account"
                # email_body = "Example body"
                # send_mail(
                #     email_subject,
                #     email_body,
                #     "noreply@oong.com",
                #     [email],
                #     fail_silently=False
                # )
                
                messages.success(request, 'Registrations successfully')
                return render(request, 'authentication/register.html', self.context)

        return render(request, 'authentication/register.html', self.context)

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error' : 'Username should only alphanumeric character'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error' : 'Username already used'}, status=400)

        return JsonResponse({'username_valid': True})

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error' : 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error' : 'Email already used'}, status=400)

        return JsonResponse({'email_valid': True})

class LoginView(View):
    context = {
        'app_name': settings.APP_NAME,
        'title': 'Login'
    }

    def get(self, request):
        return render(request, 'authentication/login.html', self.context)
    
    def post(self, request):
        self.context['fieldValues'] = request.POST

        # GET DATA
        username = request.POST['username']
        password = request.POST['password']

        # VALIDATE
        if not username:
            messages.warning(request, 'Username should be not empty')
            return render(request, 'authentication/login.html', self.context)
        if not password:
            messages.warning(request, 'Password should be not empty')
            return render(request, 'authentication/login.html', self.context)

        # LOGIN PROCESS
        user = auth.authenticate(username=username, password=password)

        if user:
            if not user.is_active:
                messages.warning(request, 'This account is not active yet')
                return render(request, 'authentication/login.html', self.context)
            auth.login(request, user)
            messages.success(request, 'Login successfully')
            return redirect('expenses')

        messages.warning(request, 'Invalid credentials')

        return render(request, 'authentication/login.html', self.context)

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'Successfully logout')
        return redirect('login')