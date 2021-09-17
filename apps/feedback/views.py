from django.contrib import messages
from apps.patient.models import Patient
from apps.feedback.models import *
from utils.decorators import crm_required, role_permission_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from utils import codes

# Create your views here.

@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
def setup(request):

    object_list = Feedback.objects.all()

    context = {
        'object_list': object_list,
    }
    return render(request, 'crm/feedback_setup.html', context)


@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
def add_setup(request):

    if request.method == 'POST':
        description = request.POST.get('description')
        submit = request.POST.get('submit')

        count = Feedback.objects.count() + 1

        code = codes.feedback('{0:05}'.format(count))

        new_feedback_setup = Feedback.objects.create(
            code=code,
            description=description,
            status=1 if submit == 'Save' else 2,
            created_by=request.user
        )

        question_type_1 = request.POST.get('question_type_1')
        question_1 = request.POST.get('question_1')
        scale_count_1 = request.POST.get('scale_count_1')
        scale_start_text_1 = request.POST.get('scale_start_text_1')
        scale_middle_text_1 = request.POST.get('scale_middle_text_1')
        scale_end_text_1 = request.POST.get('scale_end_text_1')
        answer_one_1 = request.POST.get('answer_one_1')
        answer_two_1 = request.POST.get('answer_two_1')
        answer_three_1 = request.POST.get('answer_three_1')
        answer_four_1 = request.POST.get('answer_four_1')
        required_1 = request.POST.get('required_1')

        nq1 = Question.objects.create(
            feedback_code=new_feedback_setup.code,
            question_type=question_type_1,
            text=question_1,
            is_required=True if required_1 == 'on' else False,
            scale_count=scale_count_1 if scale_count_1 else 0,
            scale_start_text=scale_start_text_1,
            scale_middle_text=scale_middle_text_1,
            scale_end_text=scale_end_text_1,
            choice_answer_one=answer_one_1,
            choice_answer_two=answer_two_1,
            choice_answer_three=answer_three_1,
            choice_answer_four=answer_four_1,
            created_by=request.user
        )

        question_type_2 = request.POST.get('question_type_2')
        question_2 = request.POST.get('question_2')
        scale_count_2 = request.POST.get('scale_count_2')
        scale_start_text_2 = request.POST.get('scale_start_text_2')
        scale_middle_text_2 = request.POST.get('scale_middle_text_2')
        scale_end_text_2 = request.POST.get('scale_end_text_2')
        answer_one_2 = request.POST.get('answer_one_2')
        answer_two_2 = request.POST.get('answer_two_2')
        answer_three_2 = request.POST.get('answer_three_2')
        answer_four_2 = request.POST.get('answer_four_2')
        required_2 = request.POST.get('required_2')

        if question_type_2:
            nq2 = Question.objects.create(
                feedback_code=new_feedback_setup.code,
                question_type=question_type_2,
                text=question_2,
                is_required=True if required_2 == 'on' else False,
                scale_count=scale_count_2 if scale_count_2 else 0,
                scale_start_text=scale_start_text_2,
                scale_middle_text=scale_middle_text_2,
                scale_end_text=scale_end_text_2,
                choice_answer_one=answer_one_2,
                choice_answer_two=answer_two_2,
                choice_answer_three=answer_three_2,
                choice_answer_four=answer_four_2,
                created_by=request.user
            )

        question_type_3 = request.POST.get('question_type_3')
        question_3 = request.POST.get('question_3')
        scale_count_3 = request.POST.get('scale_count_3')
        scale_start_text_3 = request.POST.get('scale_start_text_3')
        scale_middle_text_3 = request.POST.get('scale_middle_text_3')
        scale_end_text_3 = request.POST.get('scale_end_text_3')
        answer_one_3 = request.POST.get('answer_one_3')
        answer_two_3 = request.POST.get('answer_two_3')
        answer_three_3 = request.POST.get('answer_three_3')
        answer_four_3 = request.POST.get('answer_four_3')
        required_3 = request.POST.get('required_3')

        if question_type_3:
            nq3 = Question.objects.create(
                feedback_code=new_feedback_setup.code,
                question_type=question_type_3,
                text=question_3,
                is_required=True if required_3 == 'on' else False,
                scale_count=scale_count_3 if scale_count_3 else 0,
                scale_start_text=scale_start_text_3,
                scale_middle_text=scale_middle_text_3,
                scale_end_text=scale_end_text_3,
                choice_answer_one=answer_one_3,
                choice_answer_two=answer_two_3,
                choice_answer_three=answer_three_3,
                choice_answer_four=answer_four_3,
                created_by=request.user
            )

        question_type_4 = request.POST.get('question_type_4')
        question_4 = request.POST.get('question_4')
        scale_count_4 = request.POST.get('scale_count_4')
        scale_start_text_4 = request.POST.get('scale_start_text_4')
        scale_middle_text_4 = request.POST.get('scale_middle_text_4')
        scale_end_text_4 = request.POST.get('scale_end_text_4')
        answer_one_4 = request.POST.get('answer_one_4')
        answer_two_4 = request.POST.get('answer_two_4')
        answer_three_4 = request.POST.get('answer_three_4')
        answer_four_4 = request.POST.get('answer_four_4')
        required_4 = request.POST.get('required_4')

        if question_type_4:
            nq4 = Question.objects.create(
                feedback_code=new_feedback_setup.code,
                question_type=question_type_4,
                text=question_4,
                is_required=True if required_4 == 'on' else False,
                scale_count=scale_count_4 if scale_count_4 else 0,
                scale_start_text=scale_start_text_4,
                scale_middle_text=scale_middle_text_4,
                scale_end_text=scale_end_text_4,
                choice_answer_one=answer_one_4,
                choice_answer_two=answer_two_4,
                choice_answer_three=answer_three_4,
                choice_answer_four=answer_four_4,
                created_by=request.user
            )
        
        question_type_5 = request.POST.get('question_type_5')
        question_5 = request.POST.get('question_5')
        scale_count_5 = request.POST.get('scale_count_5')
        scale_start_text_5 = request.POST.get('scale_start_text_5')
        scale_middle_text_5 = request.POST.get('scale_middle_text_5')
        scale_end_text_5 = request.POST.get('scale_end_text_5')
        answer_one_5 = request.POST.get('answer_one_5')
        answer_two_5 = request.POST.get('answer_two_5')
        answer_three_5 = request.POST.get('answer_three_5')
        answer_four_5 = request.POST.get('answer_four_5')
        required_5 = request.POST.get('required_5')

        if question_type_5:
            nq5 = Question.objects.create(
                feedback_code=new_feedback_setup.code,
                question_type=question_type_5,
                text=question_5,
                is_required=True if required_5 == 'on' else False,
                scale_count=scale_count_5 if scale_count_5 else 0,
                scale_start_text=scale_start_text_5,
                scale_middle_text=scale_middle_text_5,
                scale_end_text=scale_end_text_5,
                choice_answer_one=answer_one_5,
                choice_answer_two=answer_two_5,
                choice_answer_three=answer_three_5,
                choice_answer_four=answer_four_5,
                created_by=request.user
            )
        
        question_type_6 = request.POST.get('question_type_6')
        question_6 = request.POST.get('question_6')
        scale_count_6 = request.POST.get('scale_count_6')
        scale_start_text_6 = request.POST.get('scale_start_text_6')
        scale_middle_text_6 = request.POST.get('scale_middle_text_6')
        scale_end_text_6 = request.POST.get('scale_end_text_6')
        answer_one_6 = request.POST.get('answer_one_6')
        answer_two_6 = request.POST.get('answer_two_6')
        answer_three_6 = request.POST.get('answer_three_6')
        answer_four_6 = request.POST.get('answer_four_6')
        required_6 = request.POST.get('required_6')
        
        if question_type_6:
            nq6 = Question.objects.create(
                feedback_code=new_feedback_setup.code,
                question_type=question_type_6,
                text=question_6,
                is_required=True if required_6 == 'on' else False,
                scale_count=scale_count_6 if scale_count_6 else 0,
                scale_start_text=scale_start_text_6,
                scale_middle_text=scale_middle_text_6,
                scale_end_text=scale_end_text_6,
                choice_answer_one=answer_one_6,
                choice_answer_two=answer_two_6,
                choice_answer_three=answer_three_6,
                choice_answer_four=answer_four_6,
                created_by=request.user
            )

        question_type_7 = request.POST.get('question_type_7')
        question_7 = request.POST.get('question_7')
        scale_count_7 = request.POST.get('scale_count_7')
        scale_start_text_7 = request.POST.get('scale_start_text_7')
        scale_middle_text_7 = request.POST.get('scale_middle_text_7')
        scale_end_text_7 = request.POST.get('scale_end_text_7')
        answer_one_7 = request.POST.get('answer_one_7')
        answer_two_7 = request.POST.get('answer_two_7')
        answer_three_7 = request.POST.get('answer_three_2')
        answer_four_7 = request.POST.get('answer_four_7')
        required_7 = request.POST.get('required_7')

        if question_type_7:
            nq7 = Question.objects.create(
                feedback_code=new_feedback_setup.code,
                question_type=question_type_7,
                text=question_7,
                is_required=True if required_7 == 'on' else False,
                scale_count=scale_count_7 if scale_count_7 else 0,
                scale_start_text=scale_start_text_7,
                scale_middle_text=scale_middle_text_7,
                scale_end_text=scale_end_text_7,
                choice_answer_one=answer_one_7,
                choice_answer_two=answer_two_7,
                choice_answer_three=answer_three_7,
                choice_answer_four=answer_four_7,
                created_by=request.user
            )

        question_type_8 = request.POST.get('question_type_8')
        question_8 = request.POST.get('question_8')
        scale_count_8 = request.POST.get('scale_count_8')
        scale_start_text_8 = request.POST.get('scale_start_text_8')
        scale_middle_text_8 = request.POST.get('scale_middle_text_8')
        scale_end_text_8 = request.POST.get('scale_end_text_8')
        answer_one_8 = request.POST.get('answer_one_8')
        answer_two_8 = request.POST.get('answer_two_8')
        answer_three_8 = request.POST.get('answer_three_8')
        answer_four_8 = request.POST.get('answer_four_8')
        required_8 = request.POST.get('required_8')

        if question_type_8:
            nq8 = Question.objects.create(
                feedback_code=new_feedback_setup.code,
                question_type=question_type_8,
                text=question_8,
                is_required=True if required_8 == 'on' else False,
                scale_count=scale_count_8 if scale_count_8 else 0,
                scale_start_text=scale_start_text_8,
                scale_middle_text=scale_middle_text_8,
                scale_end_text=scale_end_text_8,
                choice_answer_one=answer_one_8,
                choice_answer_two=answer_two_8,
                choice_answer_three=answer_three_8,
                choice_answer_four=answer_four_8,
                created_by=request.user
            )

        question_type_9 = request.POST.get('question_type_9')
        question_9 = request.POST.get('question_9')
        scale_count_9 = request.POST.get('scale_count_9')
        scale_start_text_9 = request.POST.get('scale_start_text_9')
        scale_middle_text_9 = request.POST.get('scale_middle_text_9')
        scale_end_text_9 = request.POST.get('scale_end_text_9')
        answer_one_9 = request.POST.get('answer_one_9')
        answer_two_9 = request.POST.get('answer_two_9')
        answer_three_9 = request.POST.get('answer_three_9')
        answer_four_9 = request.POST.get('answer_four_9')
        required_9 = request.POST.get('required_9')

        if question_type_9:
            nq9 = Question.objects.create(
                feedback_code=new_feedback_setup.code,
                question_type=question_type_9,
                text=question_9,
                is_required=True if required_9 == 'on' else False,
                scale_count=scale_count_9 if scale_count_9 else 0,
                scale_start_text=scale_start_text_9,
                scale_middle_text=scale_middle_text_9,
                scale_end_text=scale_end_text_9,
                choice_answer_one=answer_one_9,
                choice_answer_two=answer_two_9,
                choice_answer_three=answer_three_9,
                choice_answer_four=answer_four_9,
                created_by=request.user
            )
        
        question_type_10 = request.POST.get('question_type_10')
        question_10 = request.POST.get('question_10')
        scale_count_10 = request.POST.get('scale_count_10')
        scale_start_text_10 = request.POST.get('scale_start_text_10')
        scale_middle_text_10 = request.POST.get('scale_middle_text_10')
        scale_end_text_10 = request.POST.get('scale_end_text_10')
        answer_one_10 = request.POST.get('answer_one_10')
        answer_two_10 = request.POST.get('answer_two_10')
        answer_three_10 = request.POST.get('answer_three_10')
        answer_four_10 = request.POST.get('answer_four_10')
        required_10 = request.POST.get('required_10')

        if question_type_10:
            nq10 = Question.objects.create(
                feedback_code=new_feedback_setup.code,
                question_type=question_type_10,
                text=question_10,
                is_required=True if required_10 == 'on' else False,
                scale_count=scale_count_10 if scale_count_10 else 0,
                scale_start_text=scale_start_text_10,
                scale_middle_text=scale_middle_text_10,
                scale_end_text=scale_end_text_10,
                choice_answer_one=answer_one_10,
                choice_answer_two=answer_two_10,
                choice_answer_three=answer_three_10,
                choice_answer_four=answer_four_10,
                created_by=request.user
            )

        return redirect('feedback:setup')
    return render(request, 'crm/new_feedback_setup.html')


@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
def setup_details(request, uuid):

    feedback = None
    try:
        feedback = Feedback.objects.get(uuid=uuid)
    except Feedback.DoesNotExist:pass

    questions = Question.objects.filter(feedback_code=feedback.code)

    # responses = FeedbackResponse.objects.filter(feedback_code=feedback.code)

    context = {
        'object': feedback,
        'questions': questions,
        # 'responses': responses
    }

    if request.method == 'POST':
        submit = request.POST.get('submit')

        if submit == 'Publish':
            feedback.status = 2
        elif submit == 'Unpublish':
            feedback.status = 3
        
        feedback.save()

        return redirect('feedback:setup-details', uuid)

    return render(request, 'crm/feedback_setup_details.html', context)


@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
@role_permission_required("view_feedbackresponse", 'permission-error')
def feedback_responses(request):

    context = {
        'object_list': FeedbackResponse.objects.filter(branch_code=request.user.branch_code),
    }
    return render(request, 'crm/feedback_responses.html', context)


@login_required(login_url='login')
@crm_required(redirect_url='permission-error')
@role_permission_required("view_feedbackresponse", 'permission-error')
def response_details(request, uuid):

    response = None

    try:
        response = FeedbackResponse.objects.get(uuid=uuid)
    except:pass

    patient = Patient.objects.get(code=response.patient_id)
    attendances = Attendance.objects.filter(patient_code=patient.code)

    feedback = Feedback.objects.get(code=response.feedback_code)

    questions = Question.objects.filter(feedback_code=feedback.code)

    answers = Answer.objects.filter(response=response)
    context = {
        'object': response,
        'attendances': attendances,
        'questions': questions,
        'answers': answers,
    }

    if request.method == 'POST':
        
        for question in questions:
            try:
                question_answer = request.POST.get(f"{question.id}")
                print(question_answer)
                try:
                    Answer.objects.get(response=response, question=question)
                except Answer.DoesNotExist:
                    na = Answer.objects.create(
                        response=response,
                        question=question,
                        text=question_answer
                    )
            except:pass

        response.is_submitted = True
        response.submitted_by = request.user.code
        response.officer_id = request.user.code

        response.save()

        messages.success(request, f'Feedback {feedback.code} responded for patient {patient.code}')

        return redirect('feedback:response-details', uuid)
    return render(request, 'crm/feedback_response_details.html', context)