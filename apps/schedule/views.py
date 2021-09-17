from apps.schedule.models import Comment, Engagement, Planner
from apps.user.models import User
from datetime import datetime, timedelta, time
from django.utils import timezone
import time as tm
from utils.decorators import marketer_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.db.models import Q
from itertools import chain


# Create your views here.
@login_required(login_url='login')
@marketer_required(redirect_url='permission-error')
def weekly(request):
    hours = ["7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]

    hour_list = []

    for hour in hours:
        hour_list.append({'struct': tm.strptime(hour, '%H:%M'), 'hours': hour})

    week_date = []
    week = []
    week_ = []
    weekie = []
    week_num = []

    first_day = datetime.today().weekday()
    first_day = timedelta(days=first_day)
    first_day = datetime.today() - first_day

    nav = [-1, 1]

    try:
        nav[0] = int(request.GET['n']) - 1
        nav[1] = int(request.GET['n']) + 1
        delta = timedelta(days=int(request.GET['n']) * 7)
        first_day = first_day + delta
    except:pass

    for i in range(7):
        delta = timedelta(days=i)
        week.append(datetime.strftime((first_day+delta), "%a %d %b"))
        week_.append((first_day+delta).date())
        weekie.append([datetime.strftime((first_day+delta), '%A'), datetime.date(first_day+delta)])
        week_date.append(datetime.date(first_day+delta))
        week_num.append(({'date': ((first_day+delta).date()), 'day': datetime.strftime((first_day+delta), "%A")}))
    
    table = "<table class='table table-borderless table-hover'>"
    thead = "<thead><tr align='center'><th nowrap>Hour</th>"

    group_planners = Planner.objects.filter(
        group__code=request.user.code, activity_date__range=[week_date[1], week_date[6]]
    )

    created_planners = Planner.objects.filter(
        activity_date__range=[week_date[1], week_date[6]], created_by=request.user
    )

    planners = list(chain(created_planners, group_planners))
    # print(planners)
    for day in weekie:
        thead += f"<th style='color: blue' onclick=location.href='{reverse_lazy('schedule:daily')}?date={day[1]}'>{day[0]} <p class='h3' nowrap>{day[1].day}</p><hr style='background-color: blue; height: 2px'></th>" if timezone.now().date() == day[1] else f"<th nowrap  onclick=location.href='{reverse_lazy('schedule:daily')}?date={day[1]}'>{day[0]} <p class='h3'>{day[1].day}</p><hr style='opacity: 0.0'></th>" 
    thead += "</tr>"
    thead += "</thead>"
    table += thead
    tbody = f"<tbody>"
    for hour in hours:
        struct = tm.strptime(hour, "%H:%M")
        tbody += f"<tr align='center'>"
        tbody += f"<th nowrap><div style='border: 1px solid blue; border-radius: 10px'>{hour}</div></th>"
        for date in week_date:
            tbody += f"<td height='100' width='145' class='text-center' onclick=location.href='{reverse_lazy('schedule:daily')}?date={date}&time={hour}' nowrap>"
            for planner in planners:
                if planner.start_time.hour == struct.tm_hour and planner.activity_date == date:
                    tbody += f"<a href='{reverse_lazy('schedule:details', kwargs={'uuid': planner.uuid})}' title='{planner.description}' class='badge badge-info'>{time.strftime(planner.start_time, '%H:%M %p')} - {time.strftime(planner.end_time, '%H:%M %p')}</a>"
        tbody += f"</td></tr>"
    tbody += "</tbody>"
    
    table += tbody
    table += "</table>"

    results = mark_safe(table)
    # print(results)
    context = {
        'results': results,
        'nav': nav,
        'week_dates': week_date,
        'members': User.objects.all().exclude(username=request.user.username),
    }

    if request.method == 'POST':
        desc = request.POST.get('description')
        activity_date = request.POST.get('date')
        start = request.POST.get('start')
        end = request.POST.get('end')
        invites = request.POST.getlist('members')

        start_time = datetime.strptime(start, '%H:%M %p')
        end_time = datetime.strptime(end, '%H:%M %p')

        if start >= end:
            messages.error(request, 'Start time must not be greater than end time')
            return redirect('schedule:weekly')
        
        my_planners = Planner.objects.filter(activity_date=activity_date, created_by=request.user)

        group_planners = Planner.objects.filter(
            group__code=request.user.code, activity_date=activity_date
        )

        day_planners = list(chain(my_planners, group_planners))

        for planner in day_planners:
            # check time range
            if start_time.time() >= planner.start_time and end_time.time() <= planner.end_time:
                messages.error(request, 'Time range already scheduled')
                return redirect('schedule:weekly')
            # check start time and end time conflicts
            elif start_time.time() == planner.start_time or end_time.time == planner.end_time:
                messages.error(request, 'Time range conflicts 1')
                return redirect('schedule:weekly')

            elif start_time.time() >= planner.start_time and start_time.time() <= planner.end_time:
                messages.error(request, 'Time range conflicts with another schedule')
                return redirect('schedule:weekly')

            elif start_time.time() <= planner.start_time and end_time.time() >= planner.start_time:
                messages.error(request, 'Time range conflicts with another schedule')
                return redirect('schedule:weekly')


        np = Planner.objects.create(
            description=desc,
            activity_date=activity_date,
            start_time=start,
            end_time=end,
            orignal_date=activity_date,
            original_start_time=start_time,
            original_end_time=end_time,
            created_by=request.user
        )

        for invite in invites:
            try:
                user = User.objects.get(uuid=invite)
                np.group.add(user)
            except User.DoesNotExist:pass
        
        np.save()

        return redirect('schedule:weekly')

    return render(request, 'marketers/weekly.html', context)


@login_required(login_url='login')
@marketer_required(redirect_url='permission-error')
def planner_details(request, uuid):
    planner = None

    try:
        planner = Planner.objects.get(uuid=uuid, created_by=request.user)
    except Planner.DoesNotExist:
        try:
            planner = Planner.objects.get(group__code=request.user.code, uuid=uuid)
        except Planner.DoesNotExist:pass

    engagements = Engagement.objects.filter(planner=planner)

    # member_groups = User.objects.exclude(uuid=)
    
    # members = list(chain(member_groups, ))

    context = {
        'object': planner,
        'engagements': engagements,
        'members': User.objects.exclude(uuid=request.user.uuid)
    }

    try:
        remove_invite = request.GET.get('remove_invite')
        remove_engage = request.GET.get('remove_engage')

        if remove_invite:
            try:
                urs = User.objects.get(uuid=remove_invite)
                planner.group.remove(urs)
                print(urs)
                planner.save()
            except User.DoesNotExist:
                messages.error(request, f'Invalid user account') 

            return redirect('schedule:details', uuid)
            
        if remove_engage:
            try:
                eng = Engagement.objects.get(id=remove_engage, planner=planner)
                eng.delete()
            except Engagement.DoesNotExist:
                messages.error(request, f'This engagement does not exist')
            
            return redirect('schedule:details', uuid)
    except:pass

    if request.method == 'POST':
        submit = request.POST.get('submit')

        if submit == 'Comment':
            text = request.POST.get('text')

            nc = Comment.objects.create(
                text=text,
                created_by=request.user
            )

            planner.comments.add(nc)

            return redirect('schedule:details', uuid)

        elif submit == 'Add Engagement':
            engaged_with = request.POST.get('engaged_with')
            contact_person = request.POST.get('contact_person')
            full_name = request.POST.get('full_name')
            phone_number = request.POST.get('phone_number')
            email = request.POST.get('email')

            Engagement.objects.create(
                planner=planner,
                engaged_with=engaged_with,
                contact_person=contact_person,
                full_name=full_name,
                phone_number=phone_number,
                email=email,
                created_by=request.user
            )

            return redirect('schedule:details', uuid)

        elif submit == 'Reschedule':
            activity_date = request.POST.get('date')
            start = request.POST.get('start')
            end = request.POST.get('end')

            start_time = datetime.strptime(start, '%H:%M %p')
            end_time = datetime.strptime(end, '%H:%M %p')

            if start >= end:
                messages.error(request, 'Start time must not be greater than end time')
                return redirect('schedule:details', uuid)

            my_planners = Planner.objects.exclude(uuid=uuid).filter(activity_date=activity_date, created_by=request.user)

            group_planners = Planner.objects.exclude(uuid=uuid).filter(
                group__code=request.user.code, activity_date=activity_date
            )

            day_planners = list(chain(my_planners, group_planners))

            for plannerr in day_planners:
                # check time range
                if start_time.time() >= plannerr.start_time and end_time.time() <= plannerr.end_time:
                    messages.error(request, 'Time range already scheduled')
                    return redirect('schedule:details', uuid)
                # check start time and end time conflicts
                elif start_time.time() == plannerr.start_time or end_time.time == plannerr.end_time:
                    messages.error(request, 'Time range conflicts 1')
                    return redirect('schedule:details', uuid)

                elif start_time.time() >= plannerr.start_time and start_time.time() <= plannerr.end_time:
                    messages.error(request, 'Time range conflicts with another schedule')
                    return redirect('schedule:details', uuid)

                elif start_time.time() <= plannerr.start_time and end_time.time() >= plannerr.start_time:
                    messages.error(request, 'Time range conflicts with another schedule')
                    return redirect('schedule:details', uuid)

            planner.activity_date = activity_date
            planner.start_time = start
            planner.end_time = end
            planner.is_rescheduled = True
            planner.reschedule_at = timezone.now()
            planner.reschedule_by = request.user
            planner.save()

            return redirect('schedule:details', uuid)

        elif submit == 'Invite':
            invites = request.POST.getlist('members')

            for invite in invites:
                try:
                    m = planner.group.get(uuid=invite)
                    messages.error(request, f'{m} is already invited')
                except User.DoesNotExist:
                    try:
                        ur = User.objects.get(uuid=invite)
                        planner.group.add(ur)
                    except User.DoesNotExist:
                        messages.error(request, 'Invalid user account')

            # planner.group.save()
            planner.save()
            
            return redirect('schedule:details', uuid)

        elif submit == 'Report':
            report = request.POST.get('report')

            print(report)

            planner.report = report

            planner.save()
    return render(request, 'marketers/planner_details.html', context)


@login_required(login_url='login')
@marketer_required(redirect_url='permission-error')
def daily(request):
    today = datetime.strptime(request.GET.get('date'), '%Y-%m-%d') if request.GET.get('date') else timezone.now()

    ndate = today + timedelta(days=1)
    pdate = today - timedelta(days=1)

    ndate = datetime.strftime(ndate, '%Y-%m-%d')
    pdate = datetime.strftime(pdate, '%Y-%m-%d')

    day = today.day
    month = today.month
    year = today.year

    hours = ["7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]

    group_planners = Planner.objects.filter(
        group__code=request.user.code, activity_date=today
    )

    created_planners = Planner.objects.filter(
        activity_date=today, created_by=request.user
    )

    planners = list(chain(created_planners, group_planners))

    context = {
        'object_list': planners,
        'pdate': pdate,
        'ndate': ndate,
        'hours': hours,
        'today': today,
        'time': request.GET.get('time') if request.GET.get('time') else '',
        'members': User.objects.all().exclude(code=request.user.code)
    }

    if request.method == 'POST':
        desc = request.POST.get('description')
        activity_date = request.POST.get('date')
        start = request.POST.get('start')
        end = request.POST.get('end')
        invites = request.POST.getlist('members')

        start_time = datetime.strptime(start, '%H:%M %p')
        end_time = datetime.strptime(end, '%H:%M %p')

        if start >= end:
            messages.error(request, 'Start time must not be greater than end time')
            return redirect('schedule:daily')
        
        my_planners = Planner.objects.filter(activity_date=activity_date, created_by=request.user)

        group_planners = Planner.objects.filter(
            group__code=request.user.code, activity_date=activity_date
        )

        day_planners = list(chain(my_planners, group_planners))

        try:
            planner = Planner.objects.get(
                Q(Q(start_time__lte=start_time.time())&Q(end_time__gte=end_time.time())),
                created_by=request.user,
                activity_date=activity_date
            )
            messages.error(request, 'Time range already scheduled')
            print(planner)
            return render(request, 'marketers/daily.html', context)
        except Planner.DoesNotExist:
            try:
                planner = Planner.objects.get(
                    Q(Q(start_time__lte=start_time.time())&Q(end_time__gte=end_time.time())),
                    group__code=request.user.code,
                    activity_date=activity_date
                )
                messages.error(request, 'Time range already scheduled')
                print(planner)
                return render(request, 'marketers/daily.html', context)
            except Planner.DoesNotExist:pass

        try:
            planner = Planner.objects.get(
                Q(Q(start_time=start_time.time())|Q(end_time=end_time.time())),
                created_by=request.user,
                activity_date=activity_date
            )
            messages.error(request, 'Time range conflicts with another schedule 1')
            print(planner)
            return render(request, 'marketers/daily.html', context)
    
        except Planner.DoesNotExist:
            try:
                planner = Planner.objects.get(
                    Q(Q(start_time=start_time.time())|Q(end_time=end_time.time())),
                    group__code=request.user.code,
                    activity_date=activity_date
                )
                messages.error(request, 'Time range conflicts with another schedule 1')
                print(planner)
                return render(request, 'marketers/daily.html', context)
        
            except Planner.DoesNotExist:pass
        
        try:
            planner = Planner.objects.get(
                Q(Q(start_time__lte=start_time.time()) & Q(end_time__gte=start_time.time())),
                created_by=request.user,
                activity_date=activity_date
            )

            messages.error(request, 'Time range conflicts with another schedule 2')
            print(planner)
            return render(request, 'marketers/daily.html', context)
        except Planner.DoesNotExist:
            try:
                planner = Planner.objects.get(
                    Q(Q(start_time__lte=start_time.time()) & Q(end_time__gte=start_time.time())),
                    group__code=request.user.code,
                    activity_date=activity_date
                )

                messages.error(request, 'Time range conflicts with another schedule 2')
                print(planner)
                return render(request, 'marketers/daily.html', context)
            except Planner.DoesNotExist:pass

        try:
            planner = Planner.objects.get(
                Q(Q(start_time__gte=start_time.time()) & Q(start_time__lte=end_time.time())),
                created_by=request.user,
                activity_date=activity_date
            )

            messages.error(request, 'Time range conflicts with another schedule 3')
            print(planner)
            return render(request, 'marketers/daily.html', context)
        except Planner.DoesNotExist:
            try:
                planner = Planner.objects.get(
                    Q(Q(start_time__gte=start_time.time()) & Q(start_time__lte=end_time.time())),
                    group__code=request.user.code,
                    activity_date=activity_date
                )

                messages.error(request, 'Time range conflicts with another schedule 3')
                print(planner)
                return render(request, 'marketers/daily.html', context)
            except Planner.DoesNotExist:pass


        # for planner in day_planners:
        #     # check time range
        #     if start_time.time() >= planner.start_time and end_time.time() <= planner.end_time:
        #         messages.error(request, 'Time range already scheduled')
        #         return redirect('schedule:daily')
        #     # check start time and end time conflicts
        #     elif start_time.time() == planner.start_time or end_time.time == planner.end_time:
        #         messages.error(request, 'Time range conflicts')
        #         return redirect('schedule:daily')

        #     elif start_time.time() >= planner.start_time and start_time.time() <= planner.end_time:
        #         messages.error(request, 'Time range conflicts with another schedule')
        #         return redirect('schedule:daily')

        #     elif start_time.time() <= planner.start_time and end_time.time() >= planner.start_time:
        #         messages.error(request, 'Time range conflicts with another schedule')
        #         return redirect('schedule:daily')


        np = Planner.objects.create(
            description=desc,
            activity_date=activity_date,
            start_time=start,
            orignal_date=activity_date,
            original_start_time=start_time,
            original_end_time=end_time,
            end_time=end,
            created_by=request.user
        )

        for invite in invites:
            try:
                user = User.objects.get(uuid=invite)
                np.group.add(user)
            except User.DoesNotExist:pass
        
        np.save()

        # return redirect('schedule:daily')
        return render(request, 'marketers/daily.html', context)


    return render(request, 'marketers/daily.html', context)