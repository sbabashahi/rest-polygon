from django.urls import path, re_path

from authnz import views as authnz_views


urlpatterns = [
    path('register_email/', authnz_views.RegisterWithEmailView.as_view(), name='register_email'),
    path('login_email/', authnz_views.LoginEmailView.as_view(), name='login_email'),
    path('refresh_my_token/', authnz_views.RefreshTokenView.as_view(), name='refresh_token'),
    path('update_profile/', authnz_views.UpdateUserProfileView.as_view(), name='update_profile'),
]
