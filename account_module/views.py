from django.contrib.auth import login, logout
from django.http import Http404, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.utils.crypto import get_random_string
from account_module.forms import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
from account_module.models import User

from utils.email_service import send_email


# Create your views here.
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }

        return render(request, 'account_module/register_page.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'ایمیل وارد شده تکراری است')
            else:
                new_user = User(
                    email=user_email,
                    is_active=False,
                    email_active_code=get_random_string(72),
                    username=user_email
                )
                new_user.set_password(user_password)
                new_user.save()

                send_email('فعالسازی حساب کاربری', new_user.email, {'user': new_user}, 'emails/activate_account.html')
                return redirect(reverse('login_page'))

        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register_page.html', context)


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login_page.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_password = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'حساب کاربری شما فعال نمیباشد')
                else:
                    is_password_correct = user.check_password(user_password)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('home_page'))
                    else:
                        login_form.add_error('email', 'نام کاربری و یا رمز عبور وارد شده صحیح نمیباشد')
            else:
                login_form.add_error('email', 'نام کاربری و یا رمز عبور وارد شده صحیح نمیباشد')
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login_page.html', context)


class LogoutView(View):
    def get(self, request: HttpRequest):
        logout(request)
        return redirect(reverse('login_page'))


class ActivateAccountView(View):
    def get(self, request, email_active_code):

        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                # todo: Success Message
                return redirect(reverse('login_page'))
            else:
                # todo: show your account was activated
                pass
        else:
            raise Http404


class ForgetPasswordView(View):
    def get(self, request):
        forget_password_form = ForgetPasswordForm()
        context = {
            'forget_password_form': forget_password_form
        }
        return render(request, 'account_module/forget_password_page.html', context)

    def post(self, request: HttpRequest):
        forget_password_form = ForgetPasswordForm(request.POST)
        if forget_password_form.is_valid():
            user_email = forget_password_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                send_email('بازیابی کلمه عبور', user.email, {'user': user}, 'emails/forgot_password.html')
                return redirect(reverse('login_page'))
        context = {
            'forget_password_form': forget_password_form
        }
        return render(request, 'account_module/forget_password_page.html', context)


class ResetPasswordView(View):
    def get(self, request, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code)
        if user is None:
            return redirect(reverse('login_page'))
        reset_password_form = ResetPasswordForm()
        context = {
            'reset_password_form': reset_password_form,
            'user': user
        }
        return render(request, 'account_module/reset_password_page.html', context)

    def post(self, request: HttpRequest, active_code):
        reset_password_form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code)
        if reset_password_form.is_valid():
            if user is None:
                return redirect(reverse('login_page'))
            new_password = reset_password_form.cleaned_data.get('password')
            user.set_password(new_password)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))

        context = {
            'reset_password_form': reset_password_form,
            'user': user
        }
        return render(request, 'account_module/reset_password_page.html', context)
