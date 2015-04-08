from __future__ import absolute_import

from django.views import generic
from .forms import RegistrationForm, LoginForm


from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy

from braces import views

from django.contrib.auth.models import User


class HomePageView(generic.TemplateView):
    template_name = 'home.html'
    

class SignUpView(views.AnonymousRequiredMixin, views.FormValidMessageMixin, generic.CreateView,):
    form_class = RegistrationForm
    form_valid_message = 'Thanks for signing up !! go ahead and login'
    model = User
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
    
    def form_valid(self, form):
        resp = super(SignupView, self).form_valid(form)
        TaskList.objets.create(user = self.object, name = 'To Be Finished Independently')
        return resp
    
class LoginView(views.AnonymousRequiredMixin, views.FormValidMessageMixin, generic.FormView,):
    form_class = LoginForm
    form_valid_message = 'You are logged in now.Go ahead and start scheduling your tasks.'
    success_url = reverse_lazy('home')
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)

        
class LogOutView(generic.RedirectView, views.LoginRequiredMixin, views.MessageMixin):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        self.messages.success("You've been logged out. Come back soon!")
        return super(LogOutView, self).get(request, *args, **kwargs)