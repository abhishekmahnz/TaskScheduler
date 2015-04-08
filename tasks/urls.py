from __future__ import absolute_import

from django.conf.urls import patterns, url, include

from . import views

lists_patterns = patterns('',
     url(r'^$', views.TaskListListView.as_view(), name='list'),   
     url(r'^d/(?P<slug>[-\w]+)/$', views.TaskListDetailView.as_view(),
          name='detail'),
     url(r'^create/$', views.TaskListCreateView.as_view(), name='create'),
     url(r'^update/(?P<slug>[-\w]+)/$', views.TaskListUpdateView.as_view(),
         name='update'),
     url(r'^remove/(?P<tasklist_pk>\d+)/(?P<pk>\d+)/$', views.TaskListRemoveTaskView.as_view(),
         name='remove_task'),
     url(r'^s/(?P<slug>[-\w]+)/$', views.TaskListScheduleView.as_view(),
         name='schedule'),
 )

tasks_patterns = patterns(
    '',
    url('^d/(?P<slug>[-\w]+)/$', views.TaskDetailView.as_view(),
        name='detail'),
)

urlpatterns = patterns('',
     url(r'^lists/', include(lists_patterns, namespace='lists')),
     url(r'^tasks/', include(tasks_patterns, namespace='tasks')),
 )
