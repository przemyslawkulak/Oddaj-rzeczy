from django import forms
from django.conf.global_settings import DATE_INPUT_FORMATS
from django.forms import SplitDateTimeWidget, TextInput
from suit.widgets import SuitSplitDateTimeWidget

from app.models import Gift


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
