from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    time_limit = models.IntegerField(help_text="Time limit in minutes")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class ExamRules(models.Model):
    exam = models.OneToOneField(Exam, on_delete=models.CASCADE)
    rules = models.TextField()

    
class Question(models.Model):
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField(max_length=255)
    choice_a = models.CharField(max_length=200)
    choice_b = models.CharField(max_length=200)
    choice_c = models.CharField(max_length=200)
    choice_d = models.CharField(max_length=200)
    correct_choice = models.CharField(max_length=1)
    marks = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.question_text

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.user.get_full_name()
    
class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=1)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)

class HelpCenterContact(models.Model):
    contact_number = models.CharField(max_length=15, help_text="Contact number for help center")
    email = models.EmailField(help_text="Email address for help center")
    updated_at = models.DateTimeField(auto_now=True)  # Track when the details were last updated

    def __str__(self):
        return f"Help Center Contact Info (Updated: {self.updated_at})"

