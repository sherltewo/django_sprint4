from django.urls import path
from . import views

app_name = 'pages_cbv'  # Другое пространство имен

urlpatterns = [
    path('', views.StaticPageListView.as_view(), name='staticpage_list'),
    path(
        'create/',
        views.StaticPageCreateView.as_view(),
        name='staticpage_create'
    ),
    path(
        '<slug:slug>/',
        views.StaticPageDetailView.as_view(),
        name='staticpage_detail'
    ),
    path(
        '<slug:slug>/edit/',
        views.StaticPageUpdateView.as_view(),
        name='staticpage_edit'
    ),
    path(
        '<slug:slug>/delete/',
        views.StaticPageDeleteView.as_view(),
        name='staticpage_delete'
    ),
]
