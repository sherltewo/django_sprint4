from django.shortcuts import render
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import StaticPage


# Преобразуем функциональные views в CBV
class AboutView(TemplateView):
    """Страница 'О проекте'"""

    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О проекте Blogicum'
        return context


class RulesView(TemplateView):
    """Страница 'Правила'"""

    template_name = 'pages/rules.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Правила Blogicum'
        return context


def csrf_failure(request, reason=""):
    return render(request, "pages/403csrf.html", status=403)


def page_not_found(request, exception):
    return render(request, "pages/404.html", status=404)


def server_error(request):
    return render(request, "pages/500.html", status=500)


# CBV классы для статических страниц
class StaticPageListView(ListView):
    model = StaticPage
    template_name = 'pages/staticpage_list.html'
    context_object_name = 'pages'

    def get_queryset(self):
        return StaticPage.objects.filter(is_published=True)


class StaticPageDetailView(DetailView):
    model = StaticPage
    template_name = 'pages/staticpage_detail.html'
    context_object_name = 'page'

    def get_queryset(self):
        return StaticPage.objects.filter(is_published=True)


class StaticPageCreateView(
    LoginRequiredMixin, UserPassesTestMixin, CreateView
):
    model = StaticPage
    template_name = 'pages/staticpage_form.html'
    fields = ['title', 'content', 'slug', 'is_published']
    success_url = reverse_lazy('pages:staticpage_list')

    def test_func(self):
        return self.request.user.is_staff


class StaticPageUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, UpdateView
):
    model = StaticPage
    template_name = 'pages/staticpage_form.html'
    fields = ['title', 'content', 'slug', 'is_published']
    context_object_name = 'page'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy(
            'pages:staticpage_detail',
            kwargs={'slug': self.object.slug}
        )


class StaticPageDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
    model = StaticPage
    template_name = 'pages/staticpage_confirm_delete.html'
    success_url = reverse_lazy('pages:staticpage_list')
    context_object_name = 'page'

    def test_func(self):
        return self.request.user.is_staff
