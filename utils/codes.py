import datetime
from django.utils import timezone

def patient(first_name, last_name, date_of_birth, count):
    date = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d')
    created_at = timezone.now()
    code = first_name[0] + last_name[0] + str(date.year) + str(date.month) + str(date.day) + str(count) + str(created_at.second)

    return code


def branch(description, count):

    desc_list = description.split(' ')

    desc_init = ''

    for dl in desc_list:
        desc_init += dl[0]
    
    code = desc_init + count

    return code


def coupon(date_of_birth, first_name, last_name, count, workplace):
    date = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d')
    created_at = timezone.now()

    workplace_list = workplace.split(' ')
    workplace_init = ''

    for w in workplace_list:
        workplace_init += w[0]
    
    code = workplace_init + first_name[0] + last_name[0] + str(count) + str(date.year) + str(date.month) + str(date.day) + str(created_at.second)

    return code


def feedback(count):
    code = 'FT' + count

    return code


def user(count, first_name, last_name):

    code = first_name[0] + last_name[0] + (count)

    return code


def partner(count, workspace):
    workspace = workspace.split(' ')

    work_init = ''

    for wp in workspace:
        work_init += wp[0]

    code = work_init + count

    return code