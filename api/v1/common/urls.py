from django.urls import path
from . import views

urlpatterns = [
    path('login', views.CommonView.as_view({'post': 'login'}), name="login"),
    path('register', views.CommonView.as_view({'post': 'register'}), name="register"),
    path('logout/<int:use_id>', views.CommonView.as_view({'post': 'log_out'}), name="logout"),
    path('check_token', views.CommonView.as_view({'post': 'check_token'}), name="check_token"),
    path('profile_info/<int:pk>', views.CommonView.as_view({'get': 'profile_info'}), name="profile_info"),
    path('google_login', views.CommonView.as_view({'post': 'google_login'}), name="google_login"),
    path('facebook_login', views.CommonView.as_view({'post': 'facebook_login'}), name="facebook_login"),

]