from django import template
from apps.user.models import *

register = template.Library()


@register.simple_tag
def branches(region):
    return Branch.objects.filter(region=region)

@register.simple_tag
def branch(branch_code):
    try:
        return Branch.objects.get(code=branch_code)
    except Branch.DoesNotExist: return None


@register.simple_tag
def scales(scale):
    froms = []
    for i in range(1, scale+1):
        froms.append(i)

    return froms


@register.simple_tag(takes_context=True)
def has_perm(context, perm):

    user = context['user']

    if user.role:
        try:
            user.role.permissions.get(name=perm)
            return True
        except:
            return False
    elif user.is_active and user.is_superuser:
        return True


@register.simple_tag
def role_perm(role, codeperm):

    try:
        role.permissions.get(codename=codeperm)
        print('yes')
        return 'checked'
    except:
        return ''