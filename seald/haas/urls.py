from django.conf.urls import url, include
from rest_framework import routers

from haas import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^generateDummyHash/$', views.DummyHashView.as_view()),
    url(r'^calculateHash/$', views.HashView.as_view()),
    url(r'^register/$', views.UserRegister.as_view()),
]
