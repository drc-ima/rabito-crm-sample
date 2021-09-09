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
def add(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        phone_number = request.POST.get('phone_number').replace('-', '')
        email = request.POST.get('email')
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
            Attendance.objects.create(
                patient_code=patient.code,
                branch_code=patient.branch_code,
                created_by=request.user
            )
        
        messages.success(request, f"New Patient ID {patient.code} added.")
        return redirect('patient:search')

    return render(request, 'crm/add_patient.html')