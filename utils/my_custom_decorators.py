from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse


# Custom Decorators
# def permission_checker_decorator_factory(data):
#     def permission_checker_decorator(func):
#         def wrapper(request: HttpRequest, *args, **kwargs):
#             if request.user.is_authenticated and request.user.is_superuser:
#                 return func(request, *args, **kwargs)
#             else:
#                 return redirect(reverse('login_page'))
#
#         return wrapper
#
#     return permission_checker_decorator


def permission_checker_decorator(func):
    def wrapper(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('login_page'))

    return wrapper
