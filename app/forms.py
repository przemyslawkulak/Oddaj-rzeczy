from django import forms
from django.contrib.auth.models import User
from django.forms import TextInput

from app.models import Gift, Institution

TYPE = (
    (1, "dzieci"),
    (2, "samotne matki"),
    (3, "bezdomni"),
    (4, "starsi ludzie"),
    (5, "niepoełnosprawn")
)


class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class GiftForm(forms.ModelForm):
    # street =  forms.IntegerField(widget=forms.TextInput(attrs={'type'="text", 'name'="address"}))

    class Meta:
        model = Gift
        fields = ['street', 'city', 'post_code', 'phone', 'date', 'time', 'comments']
        widgets = {
            'street': TextInput(attrs={'type': "text", 'name': "address"}),
            'city': TextInput(attrs={'type': "text", 'name': "city"}),
            'post_code': TextInput(attrs={'type': "text", 'name': "postcode",
                                          'pattern': "^[0-9]{2}\-[0-9]{3}?", 'placeholder': "format '00-000'"}),
            'phone': TextInput(attrs={'type': "phone", 'name': "phone", 'pattern': '^\+?\d{9,10}',
                                      'placeholder': "format '+123456789'"}),
            'comments': forms.Textarea(attrs={'name': "more_info", 'rows': "5"}),
            'date': TextInput(attrs={'type': "date", 'name': "data"}),
            'time': TextInput(attrs={'type': "time", 'name': "time"}),
        }


class ContactForm(forms.Form):
    name = forms.CharField()
    surname = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)


class OrganizationForm(forms.ModelForm):
    type = forms.ChoiceField(choices=TYPE)

    class Meta:
        model = Institution
        exclude = ('approved',)
        widgets = {
            'name': TextInput(attrs={'type': "text", 'name': "name", 'placeholder': 'Nazwa instytucji'}),
            'address': TextInput(attrs={'type': "text", 'name': "address", 'placeholder': 'Adres'}),
            'city': TextInput(attrs={'type': "text", 'name': "city", 'placeholder': 'Miasto'}),
            'mission': forms.Textarea(attrs={'placeholder': 'Cel i misja instytucji', 'rows': "4"}),
            'type': forms.Select(choices=TYPE)
        }
