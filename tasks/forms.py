from __future__ import absolute_import

from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.utils.timezone import utc
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from crispy_forms.layout import Field, Fieldset

from . import models


class TaskListForm(forms.ModelForm):
    class Meta:
        fields = ('name',)
        model = models.TaskList

    def __init__(self, *args, **kwargs):
         super(TaskListForm, self).__init__(*args, **kwargs)
         self.helper = FormHelper()
         self.helper.layout = Layout(
             'name',
             ButtonHolder(
                 Submit('create', 'Create', css_class='btn-primary')
             )
         )
         
class TaskForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'supervisor', 'when_Deadline', 'client')
        model = models.Task

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'supervisor',
            'when_Deadline',
            'client',
            ButtonHolder(
                Submit('add', 'Add', css_class='btn-primary')
            )
        )

    def clean_when(self):
        when_Deadline = self.cleaned_data.get('when_Deadline')
        task_start = datetime.datetime(2015, 4, 07).replace(tzinfo=utc)
        task_end = datetime.datetime(2015, 4, 13, 17).replace(tzinfo=utc)
        if not task_start < when_Deadline < task_end:
            raise ValidationError("'deadline' is not applicable: either in past or too much ahead.")
        return when_Deadline
    
class TaskRatingForm(forms.ModelForm):
     class Meta:
         model = models.Task
         fields = ('task_effort_rating', 'client_funds_rating')

     def __init__(self, *args, **kwargs):
         super(TaskRatingForm, self).__init__(*args, **kwargs)
         self.helper = FormHelper()
         self.helper.layout = Layout(
             Fieldset(
                 'Rating',
                 Field('task_effort_rating', css_class='rating'),
                 Field('client_funds_rating', css_class='rating')
             ),
             ButtonHolder(
                 Submit('save', 'Save', css_class='btn-primary')
             )
         )
         
class TaskTaskListForm(forms.ModelForm):
     class Meta:
         model = models.Task
         fields = ('task_list',)

     def __init__(self, *args, **kwargs):
         super(TaskTaskListForm, self).__init__(*args, **kwargs)
         self.fields['task_list'].queryset = (
             self.instance.task_list.user.lists.all())

         self.helper = FormHelper()
         self.helper.layout = Layout(
             'task_list',
             ButtonHolder(
                 Submit('move', 'Move', css_class='btn-primary')
             )
         )