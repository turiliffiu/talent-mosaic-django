from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('skills/', include('skills.urls')),
    path('matching/', include('matching.urls')),
    path('mentorship/', include('mentorship.urls')),
    path('events/', include('events.urls')),
    path('challenges/', include('challenges.urls')),
    path('badges/', include('badges.urls')),
    path('analytics/', include('analytics.urls')),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'
