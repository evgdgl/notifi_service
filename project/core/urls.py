from django.urls import include, path, re_path
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView

from service import views

from rest_framework import routers
from rest_framework.response import Response
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Notification service",
      default_version='v1',
      description="Service for sending notifications via http",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="testing@api.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'customers', views.CustomersViewSet)
router.register(r'sendings', views.SendingViewSet)
router.register(r'messages', views.MessageViewSet)
router.register(r'commonstatistic', views.CommonStatistic, basename="commonstatistic")

urlpatterns = [
     path('admin/', admin.site.urls),
     path('', include(router.urls)),
     path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
     path('sendingstatistic/<pk>', views.SendingStatistic.as_view()),
     re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
     re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += router.urls

