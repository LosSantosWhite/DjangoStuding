from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from django.views import View
from .forms import RegisterForm, UserEditForm, ProfileEditForm
from .models import Profile, User


class Login(LoginView):
    template_name = 'login/login.html'


class MainView(View):
    template_name = 'login/main.html'

    def get(self, request):
        return render(request, self.template_name)


class RegisterView(FormView):
    template_name = 'login/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        new_user = form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        print(new_user)
        user = authenticate(username=username, password=raw_password)
        Profile.objects.create(user=new_user, city=form.cleaned_data.get('city'),
                               phone_number=form.cleaned_data.get('phone_number'),
                               date_of_birth=form.cleaned_data.get('date_of_birth'))
        login(self.request, user)
        return redirect('/')

@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user,
                                       data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'login/edit.html', context={
        'user_form':user_form, 'profile_form': profile_form
    })