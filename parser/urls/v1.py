from rest_framework import routers
from django.urls import path, include
from parser import views

router = routers.DefaultRouter()
router.register(r'shops', views.ShopView)


urlpatterns = [
    # path('parser/shop/create/'),
    # path('parser/shop/update/'),
    path('parser/parse/item/', views.ParserView.as_view({'get': 'parse_item'})),
]
urlpatterns += router.urls