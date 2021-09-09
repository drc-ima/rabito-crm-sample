from apps.feedback.models import *
from utils.decorators import crm_required
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

        nq1 = Question.objects.create(
            feedback_code=new_feedback_setup.code,
            question_type=question_type_1,
            text=question_1,
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

        if question_type_2:
            nq2 = Question.objects.create(
                feedback_code=new_feedback_setup.code,
                question_type=question_type_2,
                text=question_2,
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

        if question_type_3:
            nq3 = Question.objects.create(
                feedback_code=new_feedback_setup.code,
                question_type=question_type_3,
                text=question_3,
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

        if question_type_4:
            nq4 = Question.objects.create(
                feedback_code=new_feedback_setup.code,
                question_type=question_type_4,
                text=question_4,
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

        if question_type_5:
            nq5 = Question.objects.create(
                feedback_code=new_feedback_setup.code,
                question_type=question_type_5,
                text=question_5,
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