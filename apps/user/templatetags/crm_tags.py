from apps.feedback.models import Answer, Feedback
from apps.patient.models import Patient
from django import template
from apps.user.models import *
from apps.partner.models import *
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
def partner(user=None, code=None):
    if user:
        try:
            return Partner.objects.get(partner_user=user)
        except Partner.DoesNotExist: return None
    elif code:
        try:
            return Partner.objects.get(code=code)
        except Partner.DoesNotExist: return None


@register.simple_tag
def scales(scale):
    froms = []
    for i in range(1, scale+1):
        froms.append(i)

    return {
        'scales': froms,
        'first': froms[0],
        'last': froms[-1],
    }


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


@register.simple_tag
def patient(code):
    try:
        return Patient.objects.get(code=code)
    except:
        return None


@register.simple_tag
def feedback_setup(code):
    try:
        return Feedback.objects.get(code=code)
    except: return None

@register.simple_tag
def question_answer(response, question):
    try:
        answer = Answer.objects.get(response=response, question=question)
        return answer
    except Answer.DoesNotExist:
        return None