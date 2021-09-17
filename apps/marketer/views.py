from django.contrib import messages
from django.utils.text import slugify
from apps.user.models import User
from apps.partner.models import Partner
from apps.schedule.models import Engagement
from utils.decorators import marketer_required
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from utils import codes
# Create your views here.

@login_required(login_url='login')
@marketer_required(redirect_url='permission-error')
def dashboard(request):
    return render(request, 'marketers/dashboard.html')


@login_required(login_url='login')
@marketer_required(redirect_url='permission-error')
def engagements(request):

    context = {
        'object_list': Engagement.objects.filter(created_by=request.user)
    }

    return render(request, 'marketers/engagements.html', context)


@login_required(login_url='login')
@marketer_required(redirect_url='permission-error')
def partners(request):
    
    object_list = Partner.objects.filter(created_by=request.user)

    context = {
        'object_list': object_list
    }

    return render(request, 'marketers/partners.html', context)

@login_required(login_url='login')
@marketer_required(redirect_url='permission-error')
def add_partner(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        workplace = request.POST.get('workplace')
        location = request.POST.get('location')
        gender = request.POST.get('gender')

        try:
            User.objects.get(username=email)
            messages.error(request, 'User with this email already exists')
            return redirect('marketer:add-partner')
        except User.DoesNotExist:pass
        count = User.objects.count() + 1

        code = codes.user('{0:03}'.format(count), first_name, last_name)
        nu = User.objects.create(
            code=code,
            user_type='PU',
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            gender=gender,
            branch_code=request.user.branch_code,
            slug="-".join([slugify(first_name), slugify(last_name)])
        )

        nu.set_password('password')

        nu.save()

        count = Partner.objects.count() + 1

        code = codes.partner('{0:03}'.format(count), workplace)

        np = Partner.objects.create(
            code=code,
            partner_user=nu,
            workplace=workplace,
            created_by=request.user,
            location=location,
            branch_code=request.user.branch_code,
        )

        return redirect('marketer:partners')

    return render(request, 'marketers/new_partner.html')