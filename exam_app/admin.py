from django.contrib import admin
from .models import Student, Exam, Question,ExamRules,Submission,HelpCenterContact
# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by')
    search_fields = ('title',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'question_text')
    search_fields = ('question_text',)  
    

@admin.register(ExamRules)
class ExamRulesAdmin(admin.ModelAdmin):
    list_display = ('exam', 'formatted_rules')
    search_fields = ('exam__title', 'rules')
    
    def formatted_rules(self, obj):
        rules = obj.rules.split('\n')
        formatted = '<br>'.join(f'{i+1}. {rule}' for i, rule in enumerate(rules))
        return formatted
    formatted_rules.short_description = 'Rules'

    # Ensure HTML is rendered
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('exam',)  
        return self.readonly_fields

    def has_add_permission(self, request, obj=None):
        return True  
    

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'submitted_at')
    search_fields = ('student__user__username', 'exam__title')
    list_filter = ('exam', 'submitted_at')


@admin.register(HelpCenterContact)
class HelpCenterContactAdmin(admin.ModelAdmin):
    list_display = ('contact_number', 'email', 'updated_at')