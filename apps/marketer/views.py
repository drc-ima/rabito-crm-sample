from utils.decorators import marketer_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
@marketer_required(redirect_url='permission-error')
def dashboard(request):
    return render(request, 'marketers/dashboard.html')