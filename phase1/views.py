# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('enrollmentprocess.urls')),  # Point root URL to your app
# ]


# yourprojectname/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('enrollmentprocess.urls')), # Include your app's URLs
    ]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    