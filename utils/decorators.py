from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.shortcuts import resolve_url, redirect, render

def user_passes_test(test_func, redirect_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_redirect_url = resolve_url(redirect_url or settings.PERMISSION_REDIRECT_URL)

            return redirect(resolved_redirect_url)
            # raise PermissionDenied
        return _wrapped_view
    return decorator


def crm_required(function=None, redirect_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.user_type == 'AD',
        redirect_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def partner_required(function=None, redirect_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.user_type == 'PU',
        redirect_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def marketer_required(function=None, redirect_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.user_type == 'MU' or u.user_type == 'MAU',
        redirect_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def role_permission_required(codeperm, redirect_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        if isinstance(codeperm, str):
            perms = (codeperm,)
        else:
            perms = codeperm
        # First check if the user has the permission (even anon users)
        if user.has_role_perm(codeperm):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms, redirect_url=redirect_url)