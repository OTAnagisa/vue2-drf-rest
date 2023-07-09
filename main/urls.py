from django.urls import path

from main.views.news_views import NewsListAPIView
from main.views.product_views import ProductCategoryListAPIView, ProductAPIView, BrandListAPIView
from main.views.user_views import UserListAPIView

app_name = 'api'
urlpatterns = [
    path('news-list/', NewsListAPIView.as_view()),
    path('user-list/', UserListAPIView.as_view()),
    path('product-category/', ProductCategoryListAPIView.as_view()),
    path('brand/', BrandListAPIView.as_view()),
    path('product/', ProductAPIView.as_view()),
]