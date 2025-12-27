from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    # Теперь все URLs используют CBV
    path('about/', views.AboutView.as_view(), name='about'),
    path('rules/', views.RulesView.as_view(), name='rules'),
    path('pages/', views.StaticPageListView.as_view(), name='staticpage_list'),
    path(
        'pages/create/',
        views.StaticPageCreateView.as_view(),
        name='staticpage_create'
    ),
    path(
        'pages/<slug:slug>/',
        views.StaticPageDetailView.as_view(),
        name='staticpage_detail'
    ),
    path(
        'pages/<slug:slug>/edit/',
        views.StaticPageUpdateView.as_view(),
        name='staticpage_edit'
    ),
    path(
        'pages/<slug:slug>/delete/',
        views.StaticPageDeleteView.as_view(),
        name='staticpage_delete'
    ),
]
