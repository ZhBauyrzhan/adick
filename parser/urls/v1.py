from rest_framework import routers
from django.urls import path, include
from parser import views

router = routers.DefaultRouter()
router.register(r'shops', views.ShopView)
router.register(r'shops-xpath', views.ShopXPATH)

urlpatterns = [
    # path('parser/shop/create/'),
    # path('parser/shop/update/'),
    path('parser/parse/item/', views.ParserView.as_view({'post': 'parse_item'})),
    path('parser/parse/grid/', views.ParserView.as_view({'post': 'parse_grid'})),
]
urlpatterns += router.urls