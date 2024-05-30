from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from locations.api import LocationViewSet, GeneratePaymentKeyAPI, LocationMonitoringDataView
from users.api import UsersViewSet

router = routers.SimpleRouter()
router.register(r'users', UsersViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'locations-data', LocationMonitoringDataView, basename='location-data')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/payment/', GeneratePaymentKeyAPI.as_view({'post': 'create'}), name='payment'),
]
urlpatterns += i18n_patterns(
    path("i18n/", include("django.conf.urls.i18n")),
    path('users/', include('users.urls', namespace='users')),
    prefix_default_language=False,
)

urlpatterns += static(settings.MEDIA_URL, documenet_root=settings.MEDIA_ROOT)