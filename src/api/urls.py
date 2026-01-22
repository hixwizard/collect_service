from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

#from .views import CollectViewSet, PaymentViewSet

router_v1 = SimpleRouter()
#router_v1.register('collect', CollectViewSet)
#router_v1.register('payment', PaymentViewSet)

urlpatterns = [
    path('api/', include(router_v1.urls)),
    path('admin/', admin.site.urls),
]
