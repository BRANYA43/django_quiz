from django import forms
from django.core.exceptions import ValidationError

from .models import Choice


class QuestionInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        if not (self.instance.QUESTION_MIN_LIMIT <= len(self.forms) <= self.instance.QUESTION_MAX_LIMIT):
            raise ValidationError(
                'Questions count must be range '
                f'from {self.instance.QUESTION_MIN_LIMIT} '
                f'to {self.instance.QUESTION_MAX_LIMIT} inclusive'
            )
        order_nums = [form.instance.order_num for form in self.forms]

        for i, order_num in enumerate(order_nums):

            if not (1 <= order_num <= 100):
                raise ValidationError(
                    'Order num must be range from 1 ' 
                    f'to {self.instance.QUESTION_MAX_LIMIT} inclusive'
                )
            if i == 0 and order_num != 1:
                raise ValidationError(
                    'First order num must start 1.'
                )
            elif i != 0 and order_num - order_nums[i-1] != 1:
                raise ValidationError(
                    'Order num must increment 1 from past order num.'
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