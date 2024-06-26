from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('customer.urls')),
    path('administrations/', include('driver.urls')),
    path('chat/', include('chat.urls')),
    path('', include('notifications.urls'))
]
