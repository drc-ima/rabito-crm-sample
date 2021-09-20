from apps.user.models import Branch
from apps.commission.models import Commission, CommissionSetup, CommissionStatus
from django.contrib.auth.decorators import login_required
from utils.decorators import crm_required, role_permission_required
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils import timezone

# Create your views here.

@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
@role_permission_required("view_commissionsetup", 'permission-error')
def commission_setups(request):

    object_list = CommissionSetup.objects.all()

    context = {
        'object_list': object_list,
        'branches': Branch.objects.all()
    }

    if request.method == 'POST':
        if request.user.role and request.user.role.has_perm('change_commissionsetup'):
            submit = request.POST.get('submit')

            if submit == 'Save':
                
                branch_code = request.POST.get('branch_code')
                figure = request.POST.get('figure')

                try:
                    CommissionSetup.objects.get(branch_code=branch_code)
                    messages.error(request, "Branch already has commission setup")
                    return redirect('commission:setups')
                except:pass

                cs = CommissionSetup.objects.create(
                    branch_code=branch_code,
                    figure=figure,
                    created_by=request.user,
                    commission_type='Flat'
                )

                return redirect('commission:setups')
            elif submit == 'Edit':
                branch_code = request.POST.get('branch_code')
                figure = request.POST.get('figure')
                comm_id = request.POST.get('comm')
                comm = None
                try:
                    comm = CommissionSetup.objects.get(id=comm_id)
                except:
                    messages.error(request, 'Invalid setup selected')
                    return redirect('commission:setups')
                
                comm.branch_code = branch_code
                comm.figure = figure
                comm.modified_by = request.user
                comm.modified_at = timezone.now()

                comm.save()

                return redirect('commission:setups')
                
        else:
            return redirect('permission-error')
        


    return render(request, 'crm/commission_setups.html', context)


@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
@role_permission_required("view_commission", 'permission-error')
def all(request):
    object_list = Commission.objects.all()

    context = {
        'object_list': object_list,
    }

    return render(request, 'crm/commissions.html', context)

@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
@role_permission_required("view_commission", 'permission-error')
def generated(request):

    object_list = Commission.objects.filter(status=1)

    context = {
        'object_list': object_list,
    }

    if request.method == 'POST':
        print(request.POST)
        comm_ids = request.POST.getlist('commission')
        submit = request.POST.get('submit')
        if submit == 'Confirm':
            if comm_ids:
                for comm in comm_ids:
                    try:
                        commission = Commission.objects.get(coupon_code=comm)
                        commission.status = 2
                        commission.confirmed_by = request.user
                        commission.confirmed_at = timezone.now()
                        commission.save()
                        CommissionStatus.objects.create(
                            commission=commission,
                            status=2,
                            created_by=request.user
                        )
                        messages.success(request, f"Commission with ID {comm} successfully confirmed")
                    except Commission.DoesNotExist:
                        messages.error(request, f"Commission with ID {comm} does not exist")
            else:
                messages.info(request, f"Please select at least one commission")
        elif submit == 'Cancel':
            if comm_ids:
                for comm in comm_ids:
                    try:
                        commission = Commission.objects.get(coupon_code=comm)
                        commission.status = 4
                        commission.canceled_by = request.user
                        commission.canceled_at = timezone.now()
                        commission.save()
                        CommissionStatus.objects.create(
                            commission=commission,
                            status=4,
                            created_by=request.user
                        )
                        messages.success(request, f"Commission with ID {comm} successfully canceled")
                    except Commission.DoesNotExist:
                        messages.error(request, f"Commission with ID {comm} does not exist")
            else:
                messages.info(request, f"Please select at least one commission")

        return redirect('commission:generated')

    return render(request, 'crm/generated_commissions.html', context)


@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
@role_permission_required("view_commission", 'permission-error')
def confirmed(request):
    object_list = Commission.objects.filter(status=2)

    context = {
        'object_list': object_list,
    }

    if request.method == 'POST':
        print(request.POST)
        comm_ids = request.POST.getlist('commission')
        submit = request.POST.get('submit')
        if submit == 'Approve':
            if comm_ids:
                for comm in comm_ids:
                    try:
                        commission = Commission.objects.get(coupon_code=comm)
                        commission.status = 3
                        commission.approved_by = request.user
                        commission.approved_at = timezone.now()
                        commission.save()
                        CommissionStatus.objects.create(
                            commission=commission,
                            status=3,
                            created_by=request.user
                        )
                        messages.success(request, f"Commission with ID {comm} successfully approved")
                    except Commission.DoesNotExist:
                        messages.error(request, f"Commission with ID {comm} does not exist")
            else:
                messages.info(request, f"Please select at least one commission")
        elif submit == 'Cancel':
            if comm_ids:
                for comm in comm_ids:
                    try:
                        commission = Commission.objects.get(coupon_code=comm)
                        commission.status = 4
                        commission.canceled_by = request.user
                        commission.canceled_at = timezone.now()
                        commission.save()
                        CommissionStatus.objects.create(
                            commission=commission,
                            status=4,
                            created_by=request.user
                        )
                        messages.success(request, f"Commission with ID {comm} successfully canceled")
                    except Commission.DoesNotExist:
                        messages.error(request, f"Commission with ID {comm} does not exist")
            else:
                messages.info(request, f"Please select at least one commission")

        return redirect('commission:confirmed')


    return render(request, 'crm/confirmed_commissions.html', context)


@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
@role_permission_required("view_commission", 'permission-error')
def approved(request):
    object_list = Commission.objects.filter(status=3)

    context = {
        'object_list': object_list,
    }

    return render(request, 'crm/approved_commissions.html', context)


@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
@role_permission_required("view_commission", 'permission-error')
def canceled(request):
    object_list = Commission.objects.filter(status=4)

    context = {
        'object_list': object_list,
    }

    return render(request, 'crm/canceled_commissions.html', context)