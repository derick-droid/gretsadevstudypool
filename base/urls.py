from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("room/<str:pk>/", views.room, name="room"),
    path("profile/<str:pk>", views.userProfile, name = "user-profile"),
    path("create_room/", views.create_room, name="create_room"),
    path("update_room/<str:pk>/", views.update_room, name="update_room"),
    path("delete_room/<str:pk>/", views.delete_room, name="delete_room"),
    path("login_page/", views.login_page, name="login_page"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path("register/", views.register_user, name="register"),
    path("delete_message/<str:pk>/", views.delete_message, name="delete_message"),

]