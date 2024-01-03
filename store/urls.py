from django.urls import path
from .views import *
app_name="store"
urlpatterns=[
    path('',HomeView.as_view(),name="home"),
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('cart/',CartView.as_view(),name="cart"),
    path('register/',RegisterView.as_view(),name="register"),
    path('confirm-email/<str:token>/',ConfirmEmail.as_view(),name="confirm"),
    path('login/otpcode/',OTPVerification.as_view(),name="otpverify"),
    path('bookdetail/<int:book_id>/',BookDetail.as_view(),name="bookdetail"),
]