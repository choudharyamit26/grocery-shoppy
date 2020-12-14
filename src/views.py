from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, CreateView
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from .forms import SignUpForm
from .models import User

user = get_user_model()


class HomeView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(self.request, 'index.html')

    def post(self, request, *args, **kwargs):
        print(self.request.POST)
        name = self.request.POST.get('name' or None)
        email = self.request.POST.get('email' or None)
        password = self.request.POST.get('password' or None)
        confirm_password = self.request.POST.get('confirm_password' or None)
        if name and email and password and confirm_password:
            if password != confirm_password:
                messages.info(self.request, 'Password and Confirm password did not match')
                return redirect(self.request.path_info)
            else:
                user_obj = User.objects.create(
                    name=name,
                    email=email
                )
                user_obj.set_password(password)
                user_obj.save()
        else:
            try:
                user_object = user.objects.get(email=email)
                if user_object.check_password(password):
                    login(self.request, user_object)
                    messages.success(self.request, 'Logged in successfully')
                    return redirect('src:home')
                else:
                    messages.error(self.request, "Incorrect Password")
                    # return render(request, 'login.html', {"status": 400})
                    return redirect(self.request.path_info)
            except Exception as e:
                print(e)
                messages.error(self.request, "User doesn't exists. Please sign up")
                return redirect(self.request.path_info)
        return redirect('src:home')


class AboutUs(TemplateView):
    template_name = 'about.html'

    def post(self, request, *args, **kwargs):
        print(self.request.POST)
        name = self.request.POST.get('name' or None)
        email = self.request.POST.get('email' or None)
        password = self.request.POST.get('password' or None)
        confirm_password = self.request.POST.get('confirm_password' or None)
        if name and email and password and confirm_password:
            if password != confirm_password:
                messages.info(self.request, 'Password and Confirm password did not match')
                return redirect(self.request.path_info)
            else:
                user_obj = User.objects.create(
                    name=name,
                    email=email
                )
                user_obj.set_password(password)
                user_obj.save()
        else:
            try:
                user_object = user.objects.get(email=email)
                if user_object.check_password(password):
                    login(self.request, user_object)
                    messages.success(self.request, 'Logged in successfully')
                    return redirect('src:home')
                else:
                    messages.error(self.request, "Incorrect Password")
                    # return render(request, 'login.html', {"status": 400})
                    return redirect(self.request.path_info)
            except Exception as e:
                print(e)
                messages.error(self.request, "User doesn't exists. Please sign up")
                return redirect(self.request.path_info)
        return redirect('src:home')


class SignUpView(CreateView):
    model = User
    template_name = 'base.html'
    success_url = 'src:home'
    form_class = SignUpForm
