from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import redirect
from braces import views
from django.contrib import messages
from django.db.models import Count

from . import models, forms
# Create your views here.


class RestrictToUserMixin(object):
    def get_queryset(self):
        queryset = super(RestrictToUserMixin, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset



class TaskListDetailView(views.LoginRequiredMixin,
    views.PrefetchRelatedMixin,
    generic.DetailView
    ):
    form_class = forms.TaskForm
    http_method_names = ['get', 'post']
    model = models.TaskList
    prefetch_related = ('tasks',)

    def get_context_data(self, **kwargs):
        context = super(TaskListDetailView, self).get_context_data(**kwargs)
        context.update({'form': self.form_class(self.request.POST or None)})
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = self.get_object()
            task = form.save(commit=False)
            task.task_list = obj
            task.save()            
        else:
            return self.get(request, *args, **kwargs)
        return redirect(obj)


class TaskListListView(views.LoginRequiredMixin, generic.ListView):
    model = models.TaskList

    def get_queryset(self):
        queryset = super(TaskListListView, self).get_queryset()
        queryset = queryset.annotate(talk_count=Count('tasks'))
        return self.request.user.lists.all()
      
    
class TaskListCreateView(views.LoginRequiredMixin, views.SetHeadlineMixin,
     generic.CreateView):
     form_class = forms.TaskListForm
     headline = 'Create'
     model = models.TaskList

     def form_valid(self, form):
         self.object = form.save(commit=False)
         self.object.user = self.request.user
         self.object.save()
         return super(TaskListCreateView, self).form_valid(form)
        
class TaskListUpdateView(
    #RestrictToOwnerMixin,
    views.LoginRequiredMixin,
    views.SetHeadlineMixin,
    generic.UpdateView
):
    form_class = forms.TaskListForm
    headline = 'Update'
    model = models.TaskList
    
class TaskListRemoveTaskView(
    views.LoginRequiredMixin,
    generic.RedirectView
):
    model = models.Task

    def get_redirect_url(self, *args, **kwargs):
        return self.tasklist.get_absolute_url()

    def get_object(self, pk, tasklist_pk):
        try:
            task = self.model.objects.get(
                pk=pk,
                task_list_id=tasklist_pk,
                task_list__user=self.request.user
            )
        except models.Task.DoesNotExist:
            raise Http404
        else:
            return task

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(kwargs.get('pk'),
                                      kwargs.get('tasklist_pk'))
        self.tasklist = self.object.task_list
        messages.success(
            request,
            u'{0.name} was removed from {1.name}'.format(
                self.object, self.tasklist))
        self.object.delete()
        return super(TaskListRemoveTaskView, self).get(request, *args,
                                                       **kwargs)


class TaskListScheduleView(
    RestrictToUserMixin,
    views.PrefetchRelatedMixin,
    generic.DetailView
):
    model = models.TaskList
    prefetch_related = ('tasks',)
    template_name = 'tasks/schedule.html'


class TaskDetailView(views.LoginRequiredMixin, generic.DetailView):
        model = models.Task

        def get_queryset(self):
            return self.model.objects.filter(task_list__user=self.request.user)
        
        def get_context_data(self, **kwargs):
            context = super(TaskDetailView, self).get_context_data(**kwargs)
            obj = context['object']
            list_form = forms.TaskTaskListForm(self.request.POST or None,
                                               instance=obj)
            rating_form = forms.TaskRatingForm(self.request.POST or None,
                                           instance=obj)
            context.update({
            'rating_form': rating_form,
            'list_form': list_form
            })
            return context
        # This method gives error that 'Task' is not iterable
        def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            if 'save' in request.POST:
                task_form = forms.TaskRatingForm(request.POST or None,
                                         instance=self.object)
                if task_form.is_valid():
                    task_form.save()

            if 'move' in request.POST:
                list_form = forms.TaskTaskListForm(request.POST or None,
                                           instance=self.object, user=request.user)
                if list_form.is_valid():
                    list_form.save()

            return redirect(self.object)