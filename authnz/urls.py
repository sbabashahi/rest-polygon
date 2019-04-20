from django.urls import path, re_path

from authnz import views as authnz_views


urlpatterns = [
    path('register_email/', authnz_views.RegisterWithEmailView.as_view()),
    path('login_email/', authnz_views.LoginEmailView.as_view()),
    path('refresh_my_token/', authnz_views.RefreshTokenView.as_view()),
    path('update_profile/', authnz_views.UpdateUserProfileView.as_view()),
]
