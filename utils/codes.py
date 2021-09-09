import datetime

def patient(first_name, last_name, date_of_birth, count):
    date = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d')

    code = first_name[0] + last_name[0] + str(date.year) + str(date.month) + str(date.day) + str(count)

    return code


def branch(description, count):

    desc_list = description.split(' ')

    desc_init = ''

    for dl in desc_list:
        desc_init += dl[0]
    
    code = desc_init + count

    return code


def feedback(count):
    code = 'FT' + count

    return code


def user(count, first_name, last_name):

    code = first_name[0] + last_name[0] + (count)

    return code