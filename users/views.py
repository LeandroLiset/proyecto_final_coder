from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from users.forms import RegisterForm

class UserRegistration(FormView):
    template_name = 'users/registration.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:success')

    def form_valid(self, form):
        form.save()
        return super(UserRegistration, self).form_valid(form)