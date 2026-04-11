from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, get_user_model
from django.forms import ModelForm, CharField, PasswordInput
# def index(request):
#     return render(request, 'registration/test.html', {'title': 'Главная страница'})

#def RegistrUser(request):
#    return render(request, 'registration/test.html', {'title': 'Главная страница'})

# def LogoutUser(request):
#     logout(request)
#     return redirect("main:index")


class RegisterUserForm(ModelForm):
    username = CharField(label="Логин")
    password = CharField(label="Пароль", widget=PasswordInput)
    password2 = CharField(label="Повтор пароля", widget=PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username','password', 'password2']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"]) # Хешируем пароль
        if commit:
            user.save()
        return user

class Registr(CreateView):
    template_name="registration/register.html"
    form_class = RegisterUserForm

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'
    extra_context = {'title': "Авторизация"}
