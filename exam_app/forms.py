from django import forms
from django.contrib.auth.models import User
from .models import StudentAnswer,Question,Exam,HelpCenterContact


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'description', 'time_limit']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'choice_a', 'choice_b', 'choice_c', 'choice_d', 'correct_choice']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = StudentAnswer
        fields = ['question', 'choice']


class HelpCenterContactForm(forms.ModelForm):
    class Meta:
        model = HelpCenterContact
        fields = ['contact_number', 'email']


