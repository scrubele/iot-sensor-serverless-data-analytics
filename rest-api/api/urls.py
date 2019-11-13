from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import UserViewSet, FacebookLogin, FacebookConnect, ProtectedObjectViewSet, DetourPathViewSet, RobotViewSet, SensorViewSet

from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'detours', DetourPathViewSet)
router.register(r'robots', RobotViewSet)
router.register(r'sensors', SensorViewSet)

router.register(r'protected_objects', ProtectedObjectViewSet , basename='protectedobject')
protected_object_router = routers.NestedSimpleRouter(router, r'protected_objects', lookup='protectedobject')
protected_object_router.register(r'robots', RobotViewSet, base_name='protectedobjects-robots')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/registration/', include('rest_auth.registration.urls')),
    url(r'^auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^auth/facebook/connect/$', FacebookConnect.as_view(), name='fb_connect'),

]

urlpatterns += [
    url(r'^', include(router.urls)),
    url(r'^', include(protected_object_router.urls)),
]