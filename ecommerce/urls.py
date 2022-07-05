
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('basket/', include('basket.urls')),
    path('', include('account.urls')),
    path('checkout/', include('checkout.urls')),

]

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('store.urls', namespace='store')),
#     path('basket/', include('basket.urls', namespace='basket')),
# ]
# adds in the images folder as a reachable url
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
