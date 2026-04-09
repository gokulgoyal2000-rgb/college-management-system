from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('attendance/', include('attendance.urls')),
    path('marks/', include('marks.urls')),
    path('assignments/', include('assignments.urls')),
    path('notes/', include('notes.urls')),
    path('timetable/', include('timetable.urls')),
    path('notices/', include('notices.urls')),
    path('fees/', include('fees.urls')),
    path('library/', include('library.urls')),
    path('analytics/', include('analytics.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)