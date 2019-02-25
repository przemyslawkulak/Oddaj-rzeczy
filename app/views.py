from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from app.forms import LoginForm, GiftForm
from app.models import Gift, Institution


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


class Donate1View(View):
    def get(self, request):
        return render(request, 'app/form1.html')

    def post(self, request):
        l = request.POST.getlist('products')
        clothes_to_use, clothes_useless, toys, books, others = 0, 0, 0, 0, 0
        if request.POST.get('products1', False):
            clothes_to_use = 1
        if request.POST.get('products2', False):
            clothes_useless = 1
        if request.POST.get('products3', False):
            toys = 1
        if request.POST.get('products4', False):
            books = 1
        if request.POST.get('products5', False):
            others = 1
        g = Gift.objects.create(clothes_to_use=clothes_to_use, clothes_useless=clothes_useless,
                                toys=toys, books=books, others=others)
        request.session['gift'] = g.id
        return redirect('/donate2' + '#show')
        # return reverse('donate2', anchor='show')


class Donate2View(View):
    def get(self, request):
        if 'gift' in request.session:
            g = Gift.objects.get(id=request.session['gift'])
            return render(request, 'app/form2.html', {'gift': g})

        return redirect('donate1')

    def post(self, request):
        g = Gift.objects.get(id=request.session['gift'])
        if request.POST.get('clothes_to_use', False):
            clothes_to_use = request.POST.get('clothes_to_use')
            g.clothes_to_use = clothes_to_use
        if request.POST.get('clothes_useless', False):
            clothes_useless = request.POST.get('clothes_useless')
            g.clothes_useless = clothes_useless
        if request.POST.get('toys', False):
            toys = request.POST.get('toys')
            g.toys = toys
        if request.POST.get('books', False):
            books = request.POST.get('books')
            g.books = books
        if request.POST.get('others', False):
            others = request.POST.get('others')
            g.others = others
        g.save()

        return redirect('/donate3' + '#show')


class Donate3View(View):
    def get(self, request):
        if 'gift' in request.session:
            g = Gift.objects.get(id=request.session['gift'])
            return render(request, 'app/form3.html')
        return redirect('donate1')

    def post(self, request):
        if request.POST.get('organization_search', False):
            all_institution = Institution.objects.filter(name__icontains=request.POST.get('organization_search'))
            print(request.POST['localization'])

            if request.POST['localization'] == '0':
                id_list = []
                print(all_institution)
                for i in all_institution:
                    id_list.append(i.pk)
                print(id_list)
                request.session['find'] = id_list
                return redirect('donate4')
            else:
                city = request.POST['localization']
                print(all_institution)
                all_institution = all_institution.filter(city=city)
                id_list = []
                for i in all_institution:
                    id_list.append(i.pk)
                request.session['find'] = id_list
                return redirect('donate4')
        else:
            children, mothers, homeless, disabled, old = Institution.objects.none(), Institution.objects.none(), \
                                                         Institution.objects.none(), Institution.objects.none(), \
                                                         Institution.objects.none()
            if request.POST.get('children', False):
                children = Institution.objects.filter(type=1)
            if request.POST.get('mothers', False):
                mothers = Institution.objects.filter(type=2)
            if request.POST.get('homeless', False):
                homeless = Institution.objects.filter(type=3)
            if request.POST.get('disabled', False):
                disabled = Institution.objects.filter(type=4)
            if request.POST.get('old', False):
                old = Institution.objects.filter(type=5)
            all_institution = Institution.objects.none()
            all_institution = all_institution | children
            all_institution = all_institution | mothers
            all_institution = all_institution | homeless
            all_institution = all_institution | disabled
            all_institution = all_institution | old
            if request.POST['localization'] == '0':
                id_list = []
                for i in all_institution:
                    id_list.append(i.pk)
                request.session['find'] = id_list
                return redirect('/donate4' + '#show')

            else:
                city = request.POST['localization']
                all_institution = all_institution.filter(city=city)
                id_list = []
                for i in all_institution:
                    id_list.append(i.pk)
                request.session['find'] = id_list
                return redirect('/donate4' + '#show')


class Donate4View(View):
    def get(self, request):
        if request.session['find']:
            all_institution = Institution.objects.none()
            for i in request.session['find']:
                all_institution = all_institution | Institution.objects.filter(id=i)
            return render(request, 'app/form4.html', {'all_institution': all_institution})
        else:
            all_institution = Institution.objects.none()
            return render(request, 'app/form4.html', {'all_institution': all_institution})

    def post(self, request):
        i = request.POST.get('organization')
        request.session['institution'] = i
        if 'gift' in request.session:
            g = Gift.objects.get(id=request.session['gift'])
            g.institution = Institution.objects.get(id=i)
            g.save()
            print(i)
            return redirect('/donate5' + '#show')
        return redirect('donate1')


class Donate5View(View):
    def get(self, request):
        form = GiftForm(request.POST)
        return render(request, 'app/form5.html', {'form': form})

    def post(self, request):
        form = GiftForm(request.POST)
        if 'gift' in request.session:
            if form.is_valid():
                g = Gift.objects.get(id=request.session['gift'])
                g.street = form.cleaned_data['street']
                g.city = form.cleaned_data['city']
                g.post_code = form.cleaned_data['post_code']
                g.phone = form.cleaned_data['phone']
                g.date = form.cleaned_data['date']
                g.time = form.cleaned_data['time']
                g.comments = form.cleaned_data['comments']
                g.save()

            return redirect('/donate6' + '#show')
        return redirect('donate1')


class Donate6View(View):
    def get(self, request):
        if 'gift' in request.session:
            g = Gift.objects.get(id=request.session['gift'])
            return render(request, "app/form6.html", {'gift': g})
        return redirect('donate1')

    def post(self, request):
        return redirect('/donate7' + '#show')


class Donate7View(View):
    def get(self, request):
        if 'gift' in request.session:
            del request.session['gift']
        if 'institution' in request.session:
            del request.session['institution']
        if 'find' in request.session:
            del request.session['find']
        return render(request, 'app/form7.html')
