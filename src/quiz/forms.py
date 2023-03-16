from django import forms
from django.core.exceptions import ValidationError

from .models import Choice


class QuestionInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        forms_ = [form for form in self.forms if not form.cleaned_data['DELETE']]
        if not (self.instance.QUESTION_MIN_LIMIT <= len(forms_) <= self.instance.QUESTION_MAX_LIMIT):
            raise ValidationError(
                f'Questions count must be range '
                f'from {self.instance.QUESTION_MIN_LIMIT} '
                f'to {self.instance.QUESTION_MAX_LIMIT} inclusive'
            )


class ChoiceInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        num_correct_answers = sum(form.cleaned_data['is_correct'] for form in self.forms)
        if num_correct_answers == 0:
            raise ValidationError('You must selected at least 1 option.')

        if num_correct_answers == len(self.forms):
            return ValidationError('Not allowed to select all options.')


class ChoiceForm(forms.ModelForm):
    is_selected = forms.BooleanField(required=False)

    class Meta:
        model = Choice
        fields = ['text']


ChoicesFormSet = forms.modelformset_factory(
    model=Choice,
    form=ChoiceForm,
    extra=0
)