from django.urls import path
from users.views import RegistrationAPIView, LoginAPIView

app_name = "users"
urlpatterns = [
    path("register/", RegistrationAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
]