from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, CreateView

from site_module.models import SiteSetting
from .forms import ContactUsForm, ContactUsModelForm  # , ProfileForm
from django.urls import reverse

from .models import ContactUs, UserProfile


# Create your views here.

# class base views

class ContactUsView(FormView):
    template_name = 'contact_module/contact_us_page.html'
    form_class = ContactUsModelForm
    success_url = '/contact-us/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting: SiteSetting = SiteSetting.objects.filter(is_main_settings=True).first()
        context['site_setting'] = setting
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# class ContactUsView(View):
#
#     def get(self, request):
#         contact_form = ContactUsModelForm()
#         return render(request, 'contact_module/contact_us_page.html', {
#             'contact_form': contact_form
#         })
#
#     def post(self, request):
#         contact_form = ContactUsModelForm(request.POST)
#         if contact_form.is_valid():
#             contact_form.save()
#             return redirect('home_page')
#         return render(request, 'contact_module/contact_us_page.html', {
#             'contact_form': contact_form
#         })


# function base views
# def contact_us_page(request):
#     if request.method == 'POST':
#         # contact_form = ContactUsForm(request.POST)
#         contact_form = ContactUsModelForm(request.POST)
#         if contact_form.is_valid():
#             # print(contact_form.cleaned_data)
#             # contact = ContactUs(
#             #     title=contact_form.cleaned_data.get('title'),
#             #     full_name=contact_form.cleaned_data.get('full_name'),
#             #     email=contact_form.cleaned_data.get('email'),
#             #     message=contact_form.cleaned_data.get('message')
#             # )
#             # contact.save()
#             contact_form.save()
#             return redirect('home_page')
#     else:
#         # contact_form = ContactUsForm()
#         contact_form = ContactUsModelForm()
#     return render(request, 'contact_module/contact_us_page.html', {
#         'contact_form': contact_form
#     })


class TestUserProfile(CreateView):
    template_name = 'contact_module/test_profile.html'
    model = UserProfile
    fields = '__all__'
    success_url = '/contact-us/create-profile'

# class TestUserProfile(View):
#     def get(self, request):
#         form = ProfileForm()
#         return render(request, 'contact_module/test_profile.html', {
#             'form': form
#         })
#
#     def post(self, request):
#         submitted_form = ProfileForm(request.POST, request.FILES)
#         if submitted_form.is_valid():
#             profile = UserProfile(image=request.FILES["user_image"])
#             profile.save()
#             return redirect('/contact-us/create-profile')
#
#         return render(request, 'contact_module/test_profile.html', {
#             'form': submitted_form
#         })
