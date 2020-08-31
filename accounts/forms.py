from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from accounts.models import Worker, Manager

userTypeChoices = (('1', 'Campaign Manager'), ('1', 'Worker'))

User = get_user_model()

class WorkerSignUpForm(UserCreationForm): 
    email = forms.EmailField(max_length=200)

    class Meta: 
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    # One option is to override save method. 
    # https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html
    # def save(self): 
        # user = super().save(commit=False)
        # worker = Worker(
        # pass



class ManagerSignUpForm(UserCreationForm): 
    email = forms.EmailField(max_length=200)

    class Meta: 
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

