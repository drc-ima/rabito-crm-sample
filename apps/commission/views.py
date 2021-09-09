from apps.user.models import Branch
from apps.commission.models import CommissionSetup
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