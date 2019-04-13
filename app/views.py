from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator

from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from app.forms import LoginForm, GiftForm, ContactForm, OrganizationForm
from app.models import Gift, Institution


def send_email(request):
    """
    function to sending email in contact forms
    :param request:
    :return: redirect to landing-page
    """
    form = ContactForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        surname = form.cleaned_data['surname']
        content = form.cleaned_data['content']

        send_mail(
            ('Oddaj rzeczy ' + name + ' ' + surname),
            content,
            'racemate.app@gmail.com',
            ['przemyslaw.kulak86@gmail.com'],
            fail_silently=False,
        )
        return redirect('landing-page')
    return redirect('landing-page')


class LandingPageView(LoginRequiredMixin, View):
    """
    Landing View with links to Donate Form, Adding Institution, Contact Form
    """

    def get(self, request):
        all_institutions = Institution.objects.all().filter(approved=True).order_by('?')
        p = Paginator(all_institutions, 5)
        page = request.GET.get('page')
        all_institutions_paginator = p.get_page(page)

        return render(request, 'app/index.html', {'all_institutions': all_institutions_paginator})

    def post(self, request):
        send_email(request)
        return redirect('landing-page')


class LoginView(View):
    """
    login view - if succesful redirect to landing page
    """

    def get(self, request):
        return render(request, 'app/login.html')

    def post(self, request):
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
    """
    logout view - if  if succesful redirect to login page
    """

    def get(self, request):
        logout(request)  # wylogowanie
        return redirect('login')


class RegisterView(View):
    """
    register view to creating user - if succesful redirect to login page
    check unique of username and email,
    """

    def get(self, request):
        return render(request, 'app/register.html')

    def post(self, request):
        username = request.POST.get("login")
        email = request.POST.get('email')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password2')
        users = User.objects.all()
        usernames = []
        emails = []
        for i in users:
            emails.append(i.email)
            usernames.append(i.username)
        if username and email and name and surname and password and confirm_password and password == confirm_password:
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


class ProfileView(LoginRequiredMixin, View):
    """
    Update user's details and passwords
    check unique username, email
    """

    def get(self, request):
        return render(request, 'app/profile.html')

    def post(self, request):
        send_email(request)
        username = request.POST.get("login")
        email = request.POST.get('email')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password2')
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
                return redirect('profile_update')

        if password or confirm_password:
            if password and confirm_password and password == confirm_password:
                if u.check_password(request.POST['pastpassword']):  # sprawdza stare hasło
                    u.set_password(password)  # zmienia hasło na nowe
                    update_session_auth_hash(request, u)  # nie wylogowuje po aktualizacji hasła
                    u.save()
                    text = 'Udana aktualizacja hasła'
                    return render(request, 'app/profile.html', {"text": text})
                text = 'Nieprawidłowe stare hasło'
                return render(request, 'app/profile.html', {"text": text})
            else:
                text = 'Żle powtórzone hasło'
                return render(request, 'app/profile.html', {"text": text})

        text = 'Uzupełnij dane'
        return render(request, 'app/profile.html', {"text": text})


class ProfileUpdateView(LoginRequiredMixin, View):
    """
    view to update user's details
    """
    def get(self, request):
        text = 'Udana edycja danych'
        return redirect('profile')


class Donate1View(LoginRequiredMixin, View):
    """
    View with choosing type of given donations
    """
    def get(self, request):
        return render(request, 'app/form1.html')

    def post(self, request):
        send_email(request)
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


class Donate2View(LoginRequiredMixin, View):
    """
    View to define amount of donation
    """
    def get(self, request):
        if 'gift' in request.session:
            g = Gift.objects.get(id=request.session['gift'])
            return render(request, 'app/form2.html', {'gift': g})
        return redirect('donate1')

    def post(self, request):
        send_email(request)
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


class Donate3View(LoginRequiredMixin, View):
    """
    View to select proper kind of institution, with searching engine
    """
    def get(self, request):
        if 'gift' in request.session:
            return render(request, 'app/form3.html')
        return redirect('donate1')

    def post(self, request):

        send_email(request)
        if request.POST.get('organization_search', False):
            all_institution = Institution.objects.filter(
                name__icontains=request.POST.get('organization_search')).filter(approved=True)

            if request.POST['localization'] == '0':
                id_list = []

                for i in all_institution:
                    id_list.append(i.pk)
                request.session['find'] = id_list
                return redirect('donate4')
            else:
                city = request.POST['localization']
                all_institution = all_institution.filter(city=city).filter(approved=True)
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
                children = Institution.objects.filter(type=1).filter(approved=True)
            if request.POST.get('mothers', False):
                mothers = Institution.objects.filter(type=2).filter(approved=True)
            if request.POST.get('homeless', False):
                homeless = Institution.objects.filter(type=3).filter(approved=True)
            if request.POST.get('disabled', False):
                disabled = Institution.objects.filter(type=4).filter(approved=True)
            if request.POST.get('old', False):
                old = Institution.objects.filter(type=5).filter(approved=True)
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
                all_institution = all_institution.filter(city=city).filter(approved=True)
                id_list = []
                for i in all_institution:
                    id_list.append(i.pk)
                request.session['find'] = id_list
                return redirect('/donate4' + '#show')


class Donate4View(LoginRequiredMixin, View):
    """
    View to select one institution from list of chosen on previous view
    """
    def get(self, request):
        if request.session['find']:
            all_institution = Institution.objects.none()
            for i in request.session['find']:
                all_institution = all_institution | Institution.objects.filter(id=i).filter(approved=True)
            return render(request, 'app/form4.html', {'all_institution': all_institution})
        else:
            all_institution = Institution.objects.none()
            return render(request, 'app/form4.html', {'all_institution': all_institution})

    def post(self, request):
        send_email(request)
        i = request.POST.get('organization')
        request.session['institution'] = i
        if 'gift' in request.session:
            if i:

                g = Gift.objects.get(id=request.session['gift'])
                g.institution = Institution.objects.get(id=i)
                g.save()
                return redirect('/donate5' + '#show')
            else:
                return redirect('/donate4' + '#show')
        return redirect('/donate1' + '#show')


class Donate5View(LoginRequiredMixin, View):
    """
    View to insert delivery pick up details
    """
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


class Donate6View(LoginRequiredMixin, View):
    """
    View with donate details
    """
    def get(self, request):
        if 'gift' in request.session:
            g = Gift.objects.get(id=request.session['gift'])
            return render(request, "app/form6.html", {'gift': g})
        return redirect('donate1')

    def post(self, request):
        send_email(request)
        return redirect('/donate7' + '#show')


class Donate7View(LoginRequiredMixin, View):
    """
    View with thanks, deleting session variable
    """
    def get(self, request):
        if 'gift' in request.session:
            del request.session['gift']
        if 'institution' in request.session:
            del request.session['institution']
        if 'find' in request.session:
            del request.session['find']
        return render(request, 'app/form7.html')

    def post(self, request):
        send_email(request)


class AddOrganizationView(LoginRequiredMixin, View):
    """
    View with form to add new institution
    """
    def get(self, request):
        form = OrganizationForm()
        return render(request, 'app/add_organization.html', {'form': form})

    def post(self, request):
        send_email(request)
        form = OrganizationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            mission = form.cleaned_data['mission']
            type = form.cleaned_data['type']
            institution = Institution.objects.create(name=name, address=address, city=city, mission=mission, type=type)
            send_mail(
                    'Instytucja do zatwierdzenia',
                    "Instytucja " + institution.name + " właśnie została utworzona. Proszę o zatwierdzenie",
                    'racemate.app@gmail.com',
                    ['przemyslaw.kulak86@gmail.com'],
                    fail_silently=False,
                )
            return redirect('landing-page')
        text = "Uzupełnij wszystkie dane"
        return render(request, 'app/add_organization.html', {'text': text})
