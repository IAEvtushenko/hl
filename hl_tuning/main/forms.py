from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            'first_name', 'phone', 'city', 'address', 'buying_type', 'comment'
        )


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь {username} не найден')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']


class SignUpForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['first_name'].label = 'Имя'

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Имя {username} занято')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадпают')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'phone']


class LKForm(forms.ModelForm):

    phone = forms.CharField(required=False)
    city = forms.CharField(required=False)
    address = forms.CharField(required=False)
    index = forms.CharField(required=False)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].label = 'Номер телефона'
        self.fields['first_name'].label = 'Имя'
        self.fields['city'].label = 'Город'
        self.fields['address'].label = 'Адрес'
        self.fields['index'].label = 'Индекс'
        self.fields['email'].label = 'email'

    class Meta:
        model = User
        fields = ['first_name', 'email', 'phone', 'city', 'address', 'index']