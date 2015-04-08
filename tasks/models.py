from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.timezone import utc
import mistune

# Create your models here.
class TaskList(models.Model):
    user = models.ForeignKey(User, related_name = 'lists')
    name = models.CharField(max_length = 255)
    slug = models.SlugField(max_length = 255, blank = True)
    
    
    class Meta:
        get_latest_by = "order_date"
        unique_together = ('user','name')
        
    def __unicode__(self):
        return self.name
    
    def save(self, *args,**kwargs):
        self.slug = slugify(self.name)
        super(TaskList, self).save(*args,**kwargs)
        
    def get_absolute_url(self):
        return reverse('tasks:lists:detail',kwargs={'slug':self.slug})
    
class Task(models.Model):
    CLIENT_LIST = (
        ('Manager', 'Manager'),
        ('VPD', 'VPD'),
        ('R&D', 'R&D Dept.'),
    )
    task_list = models.ForeignKey(TaskList, related_name='tasks')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    when_Deadline = models.DateTimeField()
    client = models.CharField(max_length=10, choices=CLIENT_LIST)
    supervisor = models.CharField(max_length=255)
    task_effort_rating = models.IntegerField(blank=True, default=0)
    client_funds_rating = models.IntegerField(blank=True, default=0)
    notes = models.TextField(blank=True, default='')
    notes_html = models.TextField(blank=True, default='', editable=False)

    class Meta:
        ordering = ('when_Deadline', 'client')
        unique_together = ('task_list', 'name')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.notes_html = mistune.markdown(self.notes)
        super(Task, self).save(*args, **kwargs)
        
@property
def overall_rating(self):
     if self.task_effort_rating  and self.client_funds_rating:
         return self.client_funds_rating - self.task_effort_rating
     return 0