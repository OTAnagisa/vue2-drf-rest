from django.urls import path

from main.views import NewsListAPIView, UserListAPIView

app_name = 'api'
urlpatterns = [
    path('news-list/', NewsListAPIView.as_view()),
    path('user-list/', UserListAPIView.as_view()),
]