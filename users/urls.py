from django.urls import path
from users.apps import UsersConfig
from users.views import LoginView, RegisterUserView, ConfirmVerifyUser, UserForgotPasswordView, \
    UserPasswordResetConfirmView, logout_user, UserProfileView, ModeratorListView, ModeratorUpdateUserView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('registration/', RegisterUserView.as_view(), name='registration'),
    path('confirm_registration/<str:uuid>', ConfirmVerifyUser.as_view(), name='confirm_registration'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users/all/', ModeratorListView.as_view(), name='all_user'),
    path('user/<int:pk>/', ModeratorUpdateUserView.as_view(), name='detail_user'),
]