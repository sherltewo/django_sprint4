from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from users.views import RegistrationView, ProfileEditView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('', include('pages.urls')),
    path('pages/', include('pages.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        RegistrationView.as_view(),
        name='registration',
    ),
    path(
        'profile/<str:username>/edit/',
        ProfileEditView.as_view(),
        name='profile_edit',
    ),
    # API v1
    path('api/v1/', include('api.urls')),
    # JWT-эндпоинты
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.jwt')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

handler403 = 'pages.views.csrf_failure'
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
