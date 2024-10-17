from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max
from .models import Exam, Student, Question, StudentAnswer,ExamRules,Submission,HelpCenterContact
from .forms import RegistrationForm, LoginForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def student_signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Student.objects.create(user=user, email=form.cleaned_data['email'])
            # messages.success(request, 'Registration successful. Please log in.')
            return redirect('student_login')
    else:
        form = RegistrationForm()
    return render(request, 'student_signup.html', {'form': form})


def student_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'student_login.html', {'form': form})


@login_required
def student_dashboard(request):
    user = request.user
    try:
        student = Student.objects.get(user=user)
        student_name = student.user.get_full_name() or student.user.username
    except Student.DoesNotExist:
        student_name = user.get_full_name() or user.username

    registered_students = Student.objects.count()
    total_exams = Exam.objects.count()

    context = {
        'student_name': student_name,
        'registered_students': registered_students,
        'total_exams': total_exams,
    }
    return render(request, 'student_dashboard.html', context)

@login_required
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'exam_list.html', {'exams': exams})


@login_required
def exam_details(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    exam_rules = ExamRules.objects.filter(exam=exam).first()
    
    if exam_rules:
        rules_text = exam_rules.rules
        formatted_rules = "<br>".join([f"{i+1}. {rule}" for i, rule in enumerate(rules_text.split('\n'))])
    else:
        formatted_rules = "No rules available for this exam."
    
    marks_per_question = 5
    total_marks = exam.questions.count() * marks_per_question

    context = {
        'exam': exam,
        'total_questions': exam.questions.count(),
        'total_marks': total_marks,  
        'exam_rules': formatted_rules 
    }
    
    return render(request, 'attend_exam_details.html', context)


@login_required
def start_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = Question.objects.filter(exam=exam).order_by('?')  # Shuffle questions

    context = {
        'exam': exam,
        'questions': questions,
    }

    return render(request, 'take_exam.html', context)


@login_required
def submit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    try:
        student = request.user.student
    except Student.DoesNotExist:
        messages.error(request, "Student profile is not set up. Please contact the administrator.")
        return redirect('home')  
    
    submission = Submission.objects.create(
        student=student,
        exam=exam
    )

    StudentAnswer.objects.filter(student=student, question__exam=exam).delete()

    # Iterate through all the submitted answers
    for key, value in request.POST.items():
        if key.startswith('question_') and value:  
            question_id = key.split('_')[1]
            try:
                question = get_object_or_404(Question, id=question_id, exam=exam)
                # Save the new answer with reference to the submission
                StudentAnswer.objects.create(
                    student=student,
                    question=question,
                    choice=value,
                    submission=submission  
                )
            except Question.DoesNotExist:
                messages.error(request, f"Question with ID {question_id} does not exist.")
                return redirect('exam_details', exam_id=exam_id)

    messages.success(request, "Your answers have been submitted successfully.")
    return redirect('exam_results', exam_id=exam_id)


@login_required
def exam_results(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    student = request.user.student

    try:
        latest_submission = Submission.objects.filter(student=student, exam=exam).latest('submitted_at')
        answers = StudentAnswer.objects.filter(submission=latest_submission)
    except Submission.DoesNotExist:
        messages.error(request, "No submission found for this exam.")
        return redirect('available_exams')

    correct_answers = sum(1 for answer in answers if answer.choice == answer.question.correct_choice)
    total_marks = correct_answers * 5  # Assuming each correct answer is worth 5 marks

    context = {
        'exam': exam,
        'correct_answers': correct_answers,
        'total_marks': total_marks,
    }

    return render(request, 'exam_results.html', context)


@login_required
def available_exams(request):
    student = request.user.student
    exams = Exam.objects.filter(questions__studentanswer__student=student).distinct()

    context = {
        'exams': exams
    }
    return render(request, 'available_exams.html', context)


@login_required
def view_marks(request, exam_id):
    student = request.user.student
    exam = get_object_or_404(Exam, id=exam_id)

    try:
        answers = StudentAnswer.objects.filter(student=student, question__exam=exam)
        correct_answers = sum(1 for answer in answers if answer.choice == answer.question.correct_choice)
        total_marks = correct_answers * 5
        attempts = Submission.objects.filter(student=student, exam=exam).count()
    except Submission.DoesNotExist:
        messages.error(request, "No submission found for this exam.")
        return redirect('available_exams')

    context = {
        'exam': exam,
        'total_marks': total_marks,
        'number_of_attempts': attempts
    }
    return render(request, 'view_marks.html', context)


def about(request):
    return render(request, 'about.html')


def help_center_view(request):
    contact_info = HelpCenterContact.objects.first()  # Fetch the first instance or None if not available
    return render(request, 'help_center.html', {'contact_info': contact_info})

    
def logout_view(request):
    logout(request)
    return redirect('home')