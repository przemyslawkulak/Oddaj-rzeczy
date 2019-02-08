from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from app.forms import LoginForm


class LandingPageView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'app/index.html')


# class LandingPageView(View):
#     def get(self, request):
#         return render(request, 'index.html')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'app/login.html')

    def post(self, request):
        '''

        :param request:
        :return:
        '''
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form['login'].value(),
                                # wyciągamy login i hasło z formularza i logujemy
                                password=form['password'].value())
            if user:
                login(request, user)  # logujemy
                return redirect('landing-page')
                # jeśli uda się zalogować przerzuca nas na główną stronę
            return render(request, 'app/login.html')
            # jeśli nie uda się zalogować wraca na formularz
        return render(request, 'app/login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)  # wylogowanie
        return redirect('login')


class RegisterView(View):
    def get(self, request):
        return render(request, 'app/register.html')

    def post(self, request):
        username = request.POST.get("login")
        email = request.POST.get('email')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('password2')
        users = User.objects.all()
        usernames = []
        emails = []
        for i in users:
            emails.append(i.email)
            usernames.append(i.username)
        if username and email and name and surname and password and confirmPassword and password == confirmPassword:
            if username in usernames:
                text = 'Podany user już istnieje'
                return render(request, 'app/register.html', {"text": text})
            elif email in emails:
                text = 'Podany email już istnieje'
                return render(request, 'app/register.html', {"text": text})
            else:
                User.objects.create_user(username=username,
                                         email=email,
                                         first_name=name,
                                         last_name=surname,
                                         password=password,
                                         )
                return redirect('login')
        text = 'Żle powtórzone hasło'
        return render(request, 'app/register.html', {"text": text})


class ProfileView(View):
    def get(self, request):
        return render(request, 'app/profile.html')

    def post(self, request):
        username = request.POST.get("login")
        email = request.POST.get('email')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('password2')
        u = User.objects.get(username=request.user)
        users = User.objects.all()
        usernames = []
        emails = []
        for i in users:
            emails.append(i.email)
            usernames.append(i.username)

        if username and email and name and surname:
            if username in usernames and username != request.user.username:  # sprawdza czy nie ma innych userów o tej nazwie
                text = 'Podany user już istnieje'
                return render(request, 'app/profile.html', {"text": text})
            elif email in emails and email != request.user.email:
                text = 'Podany email już istnieje'
                return render(request, 'app/profile.html', {"text": text})
            else:
                u.username = username
                u.email = email
                u.first_name = name
                u.last_name = surname
                u.save()
                text = 'Udana edycja danych'
                return render(request, 'app/profile.html', {"text": text})

        if password and confirmPassword and password == confirmPassword:
            if u.check_password(request.POST['pastpassword']):  # sprawdza stare hasło
                u.set_password(password)  # zmienia hasło na nowe
                update_session_auth_hash(request, u)  # nie wylogowuje po aktualizacji hasła
                u.save()
                text = 'Udana aktualizacja hasła'
                return render(request, 'app/profile.html', {"text": text})
            text = 'Nieprawidłowe stare hasło'
            return render(request, 'app/profile.html', {"text": text})
        text = 'Żle powtórzone hasło'
        return render(request, 'app/profile.html', {"text": text})


class DonateView(View):
    def get(self, request):
        return render(request, 'app/form.html')
