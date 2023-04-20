from django.urls import path, include

from authuser import views

urlpatterns = [
    path('profiles/', views.ProfilesList.as_view()),
    path('profiles/<slug:profile_slug>/', views.ProfileDetail.as_view()),
    path('comments/', views.CommentsList.as_view()),
    path('posts/', views.PostsList.as_view()),
    path('messages/', views.MessageList.as_view()),

]