from utils import codes
from django.http.response import HttpResponse
from utils.decorators import crm_required, role_permission_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.decorators import login_required
from . models import *
from django.utils.text import slugify
from django.db.models import Q

# Create your views here.


@login_required()
def page_not_found(request, exception=None):
    response = HttpResponse(
        template_name='404.html',
        status=404
        )
    return response


@login_required()
def server_error(request, exception=None):
    response = HttpResponse(
        template_name='500.html',
        status=500
        )
    return response


@login_required()
def bad_request(request, exception=None):
    response = HttpResponse(
        template_name='400.html',
        status=400
        )
    return response


@login_required()
def http_forbidden(request, exception=None):
    response = HttpResponse(
        template_name='403.html',
        status=403
        )
    return response


@login_required
def permission_error(request):
    if request.user.user_type == 'AD':
        return render(request, 'crm/permission_error.html')
    elif request.user.user_type == 'PU':
        return render(request, 'partners/permission_error.html')
    else:
        return render(request, 'markets/permission_error.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('user:dashboard') if request.user.user_type == 'AD' else redirect('marketer:dashboard')

    context = {
        'username': '',
        'password': '',
        'remember_me': '',
    }

    try:
        if request.session['remember_me'] == 'on':
            username = request.session['username']
            password = request.session['password']
            context['username'] = username
            context['password'] = password
            context['remember_me'] = request.session['remember_me']
    except:pass

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        try:
            user = authenticate(request=request, username=username, password=password)

            if user is None:
                messages.error(request, 'Credentials do not match')
                return redirect('login')
            elif user and user.user_type == 'PU':
                messages.error(request, 'You do not have permission to login here')
                return redirect('login')
            elif user and not user.is_active:
                messages.error(request, 'Your account has been block. Please contact admin')
                return redirect('login')
            # elif user and user.reset_password:

            login(request, user)

            user.is_loggedin = True
            user.login_at = timezone.now()
            user.status = 1
            user.save()
            
            if remember_me == 'on':
                request.session['username'] = username
                request.session['password'] = password
                request.session['remember_me'] = remember_me
            else:
                request.session['username'] = ''
                request.session['password'] = ''
                request.session['remember_me'] = 'off'

            
            redirect_to = request.POST.get(
                        'next',
                        request.GET.get('next', '')
                    )

            url_is_safe = url_has_allowed_host_and_scheme(
                url=redirect_to,
                allowed_hosts={request.get_host(), *set()},
                require_https=request.is_secure()
            )

            redirect_url = redirect_to if url_is_safe else ''

            return redirect(redirect_url) if redirect_url else redirect('user:dashboard') if user.user_type == 'AD' else redirect('marketer:dashboard')

        except:
            messages.error(request, 'Something went wrong!')
            return redirect('login')

    return render(request, 'crm/login.html', context)


@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
def dashboard(request):
    return render(request, 'crm/dashboard.html')


@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
@role_permission_required("view_branch", 'permission-error')
def branches(request):

    context = {
        'regions': REGIONS,
        'object_list': Branch.objects.all()
    }

    if request.method == 'POST':
        if request.user.role and request.user.role.has_perm('change_branch'):
            region = request.POST.get('region')
            description = request.POST.get('description')

            count = Branch.objects.count() + 1

            code = codes.branch(description, '{0:03}'.format(count))

            Branch.objects.create(region=region, code=code, description=description, created_by=request.user)

            return redirect('user:branches')

        else:
            return redirect('permission-error')
    return render(request, 'crm/branches.html', context)


@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
@role_permission_required("view_role", 'permission-error')
def roles(request):

    object_list = Role.objects.all()

    context = {
        'object_list': object_list
    }
    return render(request, 'crm/roles.html', context)


@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
@role_permission_required("change_role", 'permission-error')
def add_role(request):

    if request.method == 'POST':
        description = request.POST.get('description')

        role = Role.objects.create(description=description, created_by=request.user)

        user_read = request.POST.get('user.view_user')
        try:
            user_read_perm = Permission.objects.get(name="Can view user")
            if user_read == 'on':
                role.permissions.add(user_read_perm)
            else:
                role.permissions.remove(user_read_perm)
        except Permission.DoesNotExist:pass

        user_write = request.POST.get('user.change_user')
        try:
            user_write_perm = Permission.objects.get(name="Can change user")
            if user_write == 'on':
                role.permissions.add(user_write_perm)
            else:
                role.permissions.remove(user_write_perm)
        except Permission.DoesNotExist:pass

        role_read = request.POST.get('user.view_role')
        try:
            role_read_perm = Permission.objects.get(name="Can view Role")
            if role_read == 'on':
                role.permissions.add(role_read_perm)
            else:
                role.permissions.remove(role_read_perm)
        except Permission.DoesNotExist:pass

        role_write = request.POST.get('user.change_role')
        try:
            role_write_perm = Permission.objects.get(name="Can change Role")
            if role_write == 'on':
                role.permissions.add(role_write_perm)
            else:
                role.permissions.remove(role_write_perm)
        except Permission.DoesNotExist:pass

        branch_read = request.POST.get('user.view_branch')
        try:
            branch_read_perm = Permission.objects.get(name="Can view Branch")
            if branch_read == 'on':
                role.permissions.add(branch_read_perm)
            else:
                role.permissions.remove(branch_read_perm)
        except Permission.DoesNotExist:pass

        branch_write = request.POST.get('user.change_branch')
        try:
            branch_write_perm = Permission.objects.get(name="Can change Branch")
            if branch_write == 'on':
                role.permissions.add(branch_write_perm)
            else:
                role.permissions.remove(branch_write_perm)
        except Permission.DoesNotExist:pass

        patient_read = request.POST.get('patient.view_patient')
        try:
            patient_read_perm = Permission.objects.get(name="Can view Patient")
            if patient_read == 'on':
                role.permissions.add(patient_read_perm)
            else:
                role.permissions.remove(patient_read_perm)
        except Permission.DoesNotExist:pass

        patient_write = request.POST.get('patient.change_patient')
        try:
            patient_write_perm = Permission.objects.get(name="Can change Patient")
            if patient_write == 'on':
                role.permissions.add(patient_write_perm)
            else:
                role.permissions.remove(patient_write_perm)
        except Permission.DoesNotExist:pass

        feedback_read = request.POST.get('feedback.view_feedback')
        try:
            feedback_read_perm = Permission.objects.get(name="Can view Feedback")
            if feedback_read == 'on':
                role.permissions.add(feedback_read_perm)
            else:
                role.permissions.remove(feedback_read_perm)
        except Permission.DoesNotExist:pass

        feedback_write = request.POST.get('feedback.change_feedback')
        try:
            feedback_write_perm = Permission.objects.get(name="Can change Feedback")
            if feedback_write == 'on':
                role.permissions.add(feedback_write_perm)
            else:
                role.permissions.remove(feedback_write_perm)
        except Permission.DoesNotExist:pass

        feedbackresponse_read = request.POST.get('feedback.view_feedbackresponse')
        try:
            feedbackresponse_read_perm = Permission.objects.get(name="Can view Feedback Response")
            if feedbackresponse_read == 'on':
                role.permissions.add(feedbackresponse_read_perm)
            else:
                role.permissions.remove(feedbackresponse_read_perm)
        except Permission.DoesNotExist:pass

        feedbackresponse_write = request.POST.get('feedback.change_feedbackresponse')
        try:
            feedbackresponse_write_perm = Permission.objects.get(name="Can change Feedback Response")
            if feedbackresponse_write == 'on':
                role.permissions.add(feedbackresponse_write_perm)
            else:
                role.permissions.remove(feedbackresponse_write_perm)
        except Permission.DoesNotExist:pass

        commissionsetup_read = request.POST.get('commission.view_commissionsetup')
        try:
            commissionsetup_read_perm = Permission.objects.get(name="Can view Commission Setup")
            if commissionsetup_read == 'on':
                role.permissions.add(commissionsetup_read_perm)
            else:
                role.permissions.remove(commissionsetup_read_perm)
        except Permission.DoesNotExist:pass

        commissionsetup_write = request.POST.get('commission.change_commissionsetup')
        try:
            commissionsetup_write_perm = Permission.objects.get(name="Can change Commission Setup")
            if commissionsetup_write == 'on':
                role.permissions.add(commissionsetup_write_perm)
            else:
                role.permissions.remove(commissionsetup_write_perm)
        except Permission.DoesNotExist:pass

        commission_read = request.POST.get('commission.view_commission')
        try:
            commission_read_perm = Permission.objects.get(name="Can view Commission")
            if commission_read == 'on':
                role.permissions.add(commission_read_perm)
            else:
                role.permissions.remove(commission_read_perm)
        except Permission.DoesNotExist:pass

        commission_write = request.POST.get('commission.change_commission')
        try:
            commission_write_perm = Permission.objects.get(name="Can change Commission")
            if commission_write == 'on':
                role.permissions.add(commission_write_perm)
            else:
                role.permissions.remove(commission_write_perm)
        except Permission.DoesNotExist:pass

        role.save()

        return redirect('user:roles')

    return render(request, 'crm/add_role.html')


@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
@role_permission_required("change_role", 'permission-error')
def update_role(request, id):
    role = None
    try:
        role = Role.objects.get(id=id)
    except Role.DoesNotExist:pass

    members = User.objects.filter(role=role)
    context = {
        'object': role,
        'members': members
    }

    if request.method == 'POST':
        submit = request.POST.get('submit')

        if submit == 'Update':
            description = request.POST.get('description')
            role.description = description
            user_read = request.POST.get('user.view_user')
            try:
                user_read_perm = Permission.objects.get(name="Can view user")
                if user_read == 'on':
                    role.permissions.add(user_read_perm)
                else:
                    role.permissions.remove(user_read_perm)
            except Permission.DoesNotExist:pass

            user_write = request.POST.get('user.change_user')
            try:
                user_write_perm = Permission.objects.get(name="Can change user")
                if user_write == 'on':
                    role.permissions.add(user_write_perm)
                else:
                    role.permissions.remove(user_write_perm)
            except Permission.DoesNotExist:pass

            role_read = request.POST.get('user.view_role')
            try:
                role_read_perm = Permission.objects.get(name="Can view Role")
                if role_read == 'on':
                    role.permissions.add(role_read_perm)
                else:
                    role.permissions.remove(role_read_perm)
            except Permission.DoesNotExist:pass

            role_write = request.POST.get('user.change_role')
            try:
                role_write_perm = Permission.objects.get(name="Can change Role")
                if role_write == 'on':
                    role.permissions.add(role_write_perm)
                else:
                    role.permissions.remove(role_write_perm)
            except Permission.DoesNotExist:pass

            branch_read = request.POST.get('user.view_branch')
            try:
                branch_read_perm = Permission.objects.get(name="Can view Branch")
                if branch_read == 'on':
                    role.permissions.add(branch_read_perm)
                else:
                    role.permissions.remove(branch_read_perm)
            except Permission.DoesNotExist:pass

            branch_write = request.POST.get('user.change_branch')
            try:
                branch_write_perm = Permission.objects.get(name="Can change Branch")
                if branch_write == 'on':
                    role.permissions.add(branch_write_perm)
                else:
                    role.permissions.remove(branch_write_perm)
            except Permission.DoesNotExist:pass

            patient_read = request.POST.get('patient.view_patient')
            try:
                patient_read_perm = Permission.objects.get(name="Can view Patient")
                if patient_read == 'on':
                    role.permissions.add(patient_read_perm)
                else:
                    role.permissions.remove(patient_read_perm)
            except Permission.DoesNotExist:pass

            patient_write = request.POST.get('patient.change_patient')
            try:
                patient_write_perm = Permission.objects.get(name="Can change Patient")
                if patient_write == 'on':
                    role.permissions.add(patient_write_perm)
                else:
                    role.permissions.remove(patient_write_perm)
            except Permission.DoesNotExist:pass

            feedback_read = request.POST.get('feedback.view_feedback')
            try:
                feedback_read_perm = Permission.objects.get(name="Can view Feedback")
                if feedback_read == 'on':
                    role.permissions.add(feedback_read_perm)
                else:
                    role.permissions.remove(feedback_read_perm)
            except Permission.DoesNotExist:pass

            feedback_write = request.POST.get('feedback.change_feedback')
            try:
                feedback_write_perm = Permission.objects.get(name="Can change Feedback")
                if feedback_write == 'on':
                    role.permissions.add(feedback_write_perm)
                else:
                    role.permissions.remove(feedback_write_perm)
            except Permission.DoesNotExist:pass

            feedbackresponse_read = request.POST.get('feedback.view_feedbackresponse')
            try:
                feedbackresponse_read_perm = Permission.objects.get(name="Can view Feedback Response")
                if feedbackresponse_read == 'on':
                    role.permissions.add(feedbackresponse_read_perm)
                else:
                    role.permissions.remove(feedbackresponse_read_perm)
            except Permission.DoesNotExist:pass

            feedbackresponse_write = request.POST.get('feedback.change_feedbackresponse')
            try:
                feedbackresponse_write_perm = Permission.objects.get(name="Can change Feedback Response")
                if feedbackresponse_write == 'on':
                    role.permissions.add(feedbackresponse_write_perm)
                else:
                    role.permissions.remove(feedbackresponse_write_perm)
            except Permission.DoesNotExist:pass

            commissionsetup_read = request.POST.get('commission.view_commissionsetup')
            try:
                commissionsetup_read_perm = Permission.objects.get(name="Can view Commission Setup")
                if commissionsetup_read == 'on':
                    role.permissions.add(commissionsetup_read_perm)
                else:
                    role.permissions.remove(commissionsetup_read_perm)
            except Permission.DoesNotExist:pass

            commissionsetup_write = request.POST.get('commission.change_commissionsetup')
            try:
                commissionsetup_write_perm = Permission.objects.get(name="Can change Commission Setup")
                if commissionsetup_write == 'on':
                    role.permissions.add(commissionsetup_write_perm)
                else:
                    role.permissions.remove(commissionsetup_write_perm)
            except Permission.DoesNotExist:pass

            commission_read = request.POST.get('commission.view_commission')
            try:
                commission_read_perm = Permission.objects.get(name="Can view Commission")
                if commission_read == 'on':
                    role.permissions.add(commission_read_perm)
                else:
                    role.permissions.remove(commission_read_perm)
            except Permission.DoesNotExist:pass

            commission_write = request.POST.get('commission.change_commission')
            try:
                commission_write_perm = Permission.objects.get(name="Can change Commission")
                if commission_write == 'on':
                    role.permissions.add(commission_write_perm)
                else:
                    role.permissions.remove(commission_write_perm)
            except Permission.DoesNotExist:pass

            role.save()

        else:
            role.delete()

        return redirect('user:roles')
    return render(request, 'crm/update_role.html', context)


@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
@role_permission_required("view_user", 'permission-error')
def all_users(request):

    object_list = User.objects.all()

    context = {
        'object_list': object_list
    }

    return render(request, 'crm/all_users.html', context)


@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
@role_permission_required("view_user", 'permission-error')
def admin_users(request):
    object_list = User.objects.filter(user_type='AD')

    context = {
        'object_list': object_list
    }

    return render(request, 'crm/admin_users.html', context)


@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
@role_permission_required("view_user", 'permission-error')
def marketer_users(request):
    object_list = User.objects.filter(Q(user_type='MU')|Q(user_type='MAU'))

    context = {
        'object_list': object_list
    }

    return render(request, 'crm/marketer_users.html', context)


@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
@role_permission_required("view_user", 'permission-error')
def partner_users(request):
    object_list = User.objects.filter(user_type='PU')

    context = {
        'object_list': object_list
    }

    return render(request, 'crm/partner_users.html', context)


@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
@role_permission_required("change_user", 'permission-error')
def add_user(request):

    user_type = request.GET.get('user_type')

    context = {
        'title' : "Add " + next(item[1] for item in USER_TYPES if item[0] == user_type),
        'user_type': user_type,
        'roles': Role.objects.all(),
        'branches': Branch.objects.all(),
    }

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        profile = request.POST.get('profile')
        branch_code = request.POST.get('branch_code')
        role_id = request.POST.get('role')

        if not user_type:
            messages.error(request, 'No user type selected')
            return render(request, 'crm/add_user.html', context)

        try:
            User.objects.get(username=email)
            messages.error(request, 'Email already in use')
            return render(request, 'crm/add_user.html', context)
        except:pass

        count = User.objects.count()

        code = codes.user('{0:03}'.format(count), first_name, last_name)

        nu = User.objects.create(
            code=code,
            user_type=user_type,
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            gender=gender,
            branch_code=branch_code,
            role_id=role_id,
            slug="-".join([slugify(first_name), slugify(last_name)])
        )

        nu.set_password('password')

        nu.save()

        return redirect('user:admins') if user_type == 'AD' else redirect('user:marketers')

    return render(request, 'crm/add_user.html', context)


@login_required(login_url='login')
def user_logout(request):

    redirect_to = None
    if request.user.user_type =='AD' or request.user_type == 'MU':
        redirect_to = redirect('login')
    logout(request)

    return redirect_to

    