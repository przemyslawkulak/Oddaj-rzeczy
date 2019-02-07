from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from app.forms import LoginForm


class LandingPageView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'index.html')
# class LandingPageView(View):
#     def get(self, request):
#         return render(request, 'index.html')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html')

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
            return render(request, 'login.html')
            # jeśli nie uda się zalogować wraca na formularz
        return render(request, 'login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)  # wylogowanie
        return redirect('login')
