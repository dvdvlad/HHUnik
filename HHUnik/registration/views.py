from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm , ValidationError
from django.contrib.auth.views import LoginView, reverse_lazy
from django.contrib.auth import  get_user_model,login
from django.forms import ModelForm, CharField, PasswordInput

class RegisterUserForm(ModelForm):
    username = CharField(label="Логин")
    password = CharField(label="Пароль", widget=PasswordInput)
    password2 = CharField(label="Повтор пароля", widget=PasswordInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
    class Meta:
        model = get_user_model()
        fields = ['username','password', 'password2','isHR','phone','email']
    def clean_password2(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise ValidationError("Пароли не совпадают!")
        return p2
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class Registr(CreateView):
    template_name="registration/register.html"
    form_class = RegisterUserForm
    success_url= reverse_lazy("main:index")
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'
    extra_context = {'title': "Авторизация"}
