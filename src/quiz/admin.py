from django.contrib import admin

from .forms import ChoiceInlineFormSet, QuestionInlineFormSet
from .models import Choice, Exam, Result, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    fields = ('text', 'is_correct')
    show_change_link = True
    formset = ChoiceInlineFormSet
    extra = 0


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('text', 'exam_title', 'exam_level')
    inlines = (ChoiceInline,)

    def exam_title(self, questions):
        return questions.exam.title

    def exam_level(self, questions):
        return questions.exam.get_level_display()

    exam_title.short_description = 'exam'
    exam_level.short_description = 'level'


class QuestionInline(admin.TabularInline):
    model = Question
    fields = ('text', 'order_num')
    show_change_link = True
    extra = 0
    formset = QuestionInlineFormSet
    ordering = ('order_num',)


class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'level')
    exclude = ('uuid',)
    inlines = (QuestionInline,)


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question_text', 'is_correct')

    def question_text(self, choice):
        return choice.question.text

    question_text.short_description = 'questions'


admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Result)
admin.site.register(Question, QuestionsAdmin)
