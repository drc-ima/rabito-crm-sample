from apps.commission.models import Commission
from django.http.response import JsonResponse
from apps.partner.models import Coupon, CouponStatus, Partner
from apps.feedback.models import Feedback, FeedbackResponse
from utils import codes
from utils.decorators import crm_required, role_permission_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import *
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import *

# Create your views here.

@login_required(login_url='user:login')
@crm_required(redirect_url='permission-error')
@role_permission_required("view_patient", "permission-error")
def search(request):

    patients = None
    search = ''
    if request.GET:
        search = request.GET.get('search')
        try:
            patient = Patient.objects.get(
                Q(first_name__iexact=search) | 
                Q(last_name__iexact=search) | 
                Q(phone_number__iexact=search) | 
                Q(code=search) |
                Q(date_of_birth=search if '-' in search else None)
            )

            return redirect('patient:details', patient.uuid)
        except Patient.DoesNotExist:
            pass
        except Patient.MultipleObjectsReturned:
            patients = Patient.objects.filter(
                Q(first_name__iexact=search) | 
                Q(last_name__iexact=search) | 
                Q(phone_number__iexact=search) | 
                Q(code=search) |
                Q(date_of_birth=search if '-' in search else None)
            )
        except ValidationError:
            pass
            # messages.error(request, 'Search term invalid')
            # return redirect('patient:search')

    context = {
        'object_list': patients,
        'search': search
    }
    return render(request, 'crm/search_patients.html', context)


@login_required(login_url='user:login')
@crm_required(redirect_url='permission-error')
@role_permission_required('change_patient', 'permission-error')
def add(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        phone_number = request.POST.get('phone_number').replace('-', '')
        email = request.POST.get('email')
        coupons = request.POST.getlist('coupons')
        is_attending = request.POST.get('is_attending')

        try:
            patient = Patient.objects.get(first_name__iexact=first_name, last_name__iexact=last_name, date_of_birth=date_of_birth)
            messages.error(request, "Patient with this details already exist.")
            return render(request, 'crm/add_patient.html')
        except Patient.DoesNotExist:
            pass
        
        count = Patient.objects.count() + 1

        code = codes.patient(first_name, last_name, date_of_birth, '{0:03}'.format(count))
        patient = Patient.objects.create(
            code=code,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            email=email,
            branch_code=request.user.branch_code,
            created_by=request.user,
        )

        if is_attending == 'on':
            attendance_count = Attendance.objects.filter(patient_code=patient.code).count()
            att = Attendance.objects.create(
                patient_code=patient.code,
                branch_code=request.user.branch_code,
                created_by=request.user,
                is_first=True if attendance_count < 1 else False
            )

            feedbacks = Feedback.objects.filter(status=2)

            for feedback in feedbacks:
                FeedbackResponse.objects.create(
                    patient_id=patient.code,
                    feedback_code=feedback.code,
                    branch_code=request.user.branch_code,
                    attendance=att,
                )

        if coupons:
            for c in coupons:
                try:
                    coupon = Coupon.objects.get(code=c)
                    coupon.status = 2

                    CouponStatus.objects.create(
                        coupon=coupon,
                        status=2,
                        created_by=request.user
                    )

                    try:
                        partner = Partner.objects.get(partner_user=coupon.created_by)
                    except:pass

                    Commission.objects.create(
                        partner_code=partner.code,
                        patient_id=patient.code,
                        coupon_code=coupon.code,
                        amount=coupon.commission,
                        status=1,
                        created_by=request.user
                    )

                    coupon.save()
                except Coupon.DoesNotExist:pass
        
        messages.success(request, f"New Patient ID {patient.code} added.")
        return redirect('patient:search')

    return render(request, 'crm/add_patient.html')


@login_required(login_url='user:login')
@crm_required(redirect_url='permission-error')
def patient_details(request, uuid):
    patient = None

    try:
        patient = Patient.objects.get(uuid=uuid)
    except Patient.DoesNotExist:pass

    attendances = Attendance.objects.filter(patient_code=patient.code)

    feedbacks = FeedbackResponse.objects.filter(patient_id=patient.code)

    coupons = Coupon.objects.filter(patient_first_name__iexact=patient.first_name, patient_last_name__iexact=patient.last_name, patient_phone_number__iexact=patient.phone_number, patient_dob=patient.date_of_birth)

    context = {
        'object': patient,
        'attendances': attendances,
        'feedbacks': feedbacks,
        'coupons': coupons,
        'generated_coupons': Coupon.objects.filter(patient_first_name__iexact=patient.first_name, patient_last_name__iexact=patient.last_name, patient_phone_number__iexact=patient.phone_number, patient_dob=patient.date_of_birth, status=1)
    }

    if request.method == 'POST':
        submit = request.POST.get('submit')

        if submit == 'Record Attendance':
            coupons = request.POST.getlist('coupons')

            if coupons:
                for code in coupons:
                    try:
                        coupon = Coupon.objects.get(code=code)
                        coupon.status = 2

                        cs = CouponStatus.objects.create(
                            coupon=coupon,
                            status=2,
                            created_by=request.user
                        )

                        try:
                            partner = Partner.objects.get(partner_user=coupon.created_by)
                        except:pass

                        Commission.objects.create(
                            partner_code=partner.code,
                            patient_id=patient.code,
                            coupon_code=coupon.code,
                            amount=coupon.commission,
                            status=1,
                            created_by=request.user
                        )
                        coupon.save()
                    except Coupon.DoesNotExist:pass
            
            na = Attendance.objects.create(
                patient_code=patient.code,
                branch_code=request.user.branch_code,
                is_first=False,
            )

            feedbacks = Feedback.objects.filter(status=2)

            for feedback in feedbacks:
                FeedbackResponse.objects.create(
                    patient_id=patient.code,
                    feedback_code=feedback.code,
                    branch_code=request.user.branch_code,
                    attendance=na,
                )
            
            return redirect('patient:details', uuid)

    return render(request, 'crm/patient_details.html', context)


@login_required(login_url='user:login')
@crm_required(redirect_url='permission-error')
@role_permission_required("view_patient", "permission-error")
def patients(request):
    object_list = Patient.objects.all()

    context = {
        'object_list': object_list
    }

    return render(request, 'crm/patients.html', context)

