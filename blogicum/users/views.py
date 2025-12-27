from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from blog.models import Post


# Регистрация пользователя
class RegistrationView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


# Просмотр профиля пользователя
class ProfileView(DetailView):
    template_name = 'profile.html'
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(
            author=user
        ).order_by('-created')
        return context


# Редактирование профиля (только владелец)
class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'profile_edit.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('profile')

    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return user

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    def get_success_url(self):
        return reverse_lazy(
            'profile',
            kwargs={'username': self.object.username}
        )
