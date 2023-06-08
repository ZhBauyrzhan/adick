from django.urls import path

from users import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'user-items', views.UserItemsViewSet)

urlpatterns = [
    path('users/create/', views.UserViewSet.as_view({'post': 'create'})),
    path('users/get-all/', views.UserViewSet.as_view({'get': 'list'})),
    path('users/get/<str:username>/', views.UserViewSet.as_view({'get': 'get'})),
    path('users/destroy/<str:username>/', views.UserViewSet.as_view({'delete': 'destroy'})),
]
