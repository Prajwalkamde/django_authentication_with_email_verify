from . import views
from django.urls import path,include

urlpatterns = [
    path('', views.user_profile,name='profile'),
    path('login/', views.user_login,name='login'),
    path('signup/', views.user_signup,name='signup'),
    path('verify/<email_token>', views.user_verify,name='verify'),
    path('forget_password/' , views.ForgetPassword , name="forget_password"),
    path('change_password/<token>/' , views.ChangePassword , name="change_password"),

    # path('error', views.error_page,name='error'),
    path('logout/', views.user_logout,name='logout'),
]