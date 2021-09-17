from apps.user.models import User
from django.http.response import JsonResponse
from apps.commission.models import CommissionSetup
from apps.partner.models import Coupon
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from utils.decorators import partner_required
from django.shortcuts import redirect, render
from django.contrib import messages
from utils import codes
import datetime
from apps.user.templatetags.crm_tags import partner

# Create your views here.

@login_required(login_url='login')
@partner_required(redirect_url='permission-error')
def dashboard(request):
    return render(request, 'partners/dashboard.html')

@login_required(login_url='login')
@partner_required(redirect_url='permission-error')
def coupons(request):

    object_list = Coupon.objects.filter(created_by=request.user)

    context = {
        'object_list': object_list,
    }

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        dob = request.POST.get('dob')

        try:
            cs = CommissionSetup.objects.get(branch_code=request.user.branch_code)
        except CommissionSetup.DoesNotExist:
            messages.error(request, 'Your branch does not have any commission setup. Contact Administrator')
            return render(request, 'partners/coupons.html', context)

        partne = partner(request.user)

        count = Coupon.objects.filter(created_by=request.user).count() + 1

        code = codes.coupon(dob, first_name, last_name, '{0:02}'.format(count), partne.workplace)
        
        Coupon.objects.create(
            code=code,
            patient_first_name=first_name,
            patient_last_name=last_name,
            patient_phone_number=phone_number,
            patient_dob=dob,
            commission=cs.figure,
            branch_code=request.user.branch_code,
            created_by=request.user,
            status=1
        )

        return redirect('partner:coupons')
    return render(request, 'partners/coupons.html', context=context)

@csrf_exempt
def search_coupons(request):

    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    phone_number = request.POST.get('phone_number').replace('-', '')
    date_of_birth = request.POST.get('date_of_birth')

    coupons = Coupon.objects.filter(
        patient_first_name__iexact=first_name, patient_last_name__iexact=last_name, patient_phone_number__iexact=phone_number, patient_dob=date_of_birth, status=1
    ).values()

    clist = []
    for coupon in coupons:
        user = User.objects.get(id=coupon['created_by_id'])

        p = partner(user)

        cdict = {'code': coupon['code'], 'workplace': p.workplace, 'created_at': datetime.datetime.strftime(coupon['created_at'], '%d %B %Y, %I:%M %p')}

        clist.append(cdict)

        print(clist)

    return JsonResponse(clist, safe=False)
