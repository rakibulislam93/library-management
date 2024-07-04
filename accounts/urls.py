from django.urls import path
from .views import UserRegisterview,UserLoginView,UserLogoutView,DepositeMoney,profile,ProfileUpdate,UserPassChangeView
urlpatterns = [
    path('register/',UserRegisterview.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='loginpage'),
    path('logout',UserLogoutView.as_view(),name='logoutpage'),
    # path('profile/',UserProfile.as_view(),name='profile'),
    path('profile/',profile,name='profile'),
    path('deposite/',DepositeMoney,name='deposite'),
    path('update_profile/<int:id>/',ProfileUpdate.as_view(),name='update_profile'),
    path('password_change',UserPassChangeView.as_view(),name='pass_change'),
]
