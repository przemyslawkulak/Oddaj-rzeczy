from django import forms
from django.forms import TextInput

from app.models import Gift, Institution


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
    class Meta:
        model = Institution
        exclude = ('approved',)
        widgets = {
            'name': TextInput(attrs={'type': "text", 'name': "name", 'placeholder': 'Name'}),
            'address': TextInput(attrs={'type': "text", 'name': "address", 'placeholder': 'address'}),
            'city': TextInput(attrs={'type': "text", 'name': "city", 'placeholder': 'city'}),
            'mission': forms.Textarea(attrs={'placeholder': 'Mission'}),
        }
