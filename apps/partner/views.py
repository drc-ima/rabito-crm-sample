from apps.user.models import User
from django.http.response import JsonResponse
from apps.commission.models import Commission, CommissionSetup
from apps.partner.models import Coupon
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from utils.decorators import partner_required
from django.shortcuts import redirect, render
from django.contrib import messages
from utils import codes
import datetime
from apps.user.templatetags.crm_tags import partner
from django.core.paginator import Paginator
from django.db.models import Q
import django_filters as df
from django import forms

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


class CommissionFilter(df.FilterSet):
    start = df.DateFilter(field_name='created_at', lookup_expr='gte', widget=forms.TextInput(attrs={'data-toggle': 'datetimepicker', 'data-target': '#start', 'class': 'form-control form-control-sm datetimepicker-input', 'id': 'start'}))
    end = df.DateFilter(field_name='created_at', lookup_expr='lte', widget=forms.TextInput(attrs={'data-toggle': 'datetimepicker', 'data-target': '#end', 'class': 'form-control form-control-sm datetimepicker-input', 'id': 'end'}))

    class Meta:
        model = Commission
        fields = ('start', 'end')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.form.fields['start'].label = 'Start Date'
        self.form.fields['end'].label = 'End Date'

@login_required(login_url='login')
@partner_required(redirect_url='permission-error')
def commissions(request):

    partnerr = partner(user=request.user)
    coupon_code = ''
    end_date = None
    start_date = None

    total = 0
    object_list = Commission.objects.filter(partner_code=partnerr.code, status=3)
    try:
        coupon_code = request.GET.get('coupon')
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')
        # page_number = request.GET.get('page')
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        if coupon_code:
            object_list = Commission.objects.filter(
                Q(
                    Q(created_at__date__gte=start_date.date()) & Q(created_at__date__lte=end_date.date())
                )
                &Q(coupon_code=coupon_code),
                partner_code=partnerr.code, status=3)
        else:
            object_list = Commission.objects.filter(
                Q(
                    Q(created_at__date__gte=start_date.date()) & Q(created_at__date__lte=end_date.date())
                ),
                partner_code=partnerr.code, status=3)
    except:pass

    paginator = Paginator(object_list.order_by('-created_at'), 50)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    for obj in page_obj:
        total += obj.amount

    object_count = object_list.count()
    context = {
        'page_obj': page_obj,
        'object_count': object_count,
        'total': total,
        'coupon': coupon_code if coupon_code else '',
        'start': start_date.date() if start_date else '',
        'end': end_date.date() if end_date else '',
    }

    return render(request, 'partners/commissions.html', context)