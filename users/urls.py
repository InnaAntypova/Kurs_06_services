from django.urls import path
from users.apps import UsersConfig
from users.views import LoginView, RegisterUserView, ConfirmVerifyUser, UserForgotPasswordView, \
    UserPasswordResetConfirmView, logout_user, UserProfileUpdateView, ModeratorListView, ModeratorUpdateUserView, \
    delete_self_user, get_user_profile

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('registration/', RegisterUserView.as_view(), name='registration'),
    path('confirm_registration/<str:uuid>', ConfirmVerifyUser.as_view(), name='confirm_registration'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/', get_user_profile, name='profile_user'),
    path('profile_edit/', UserProfileUpdateView.as_view(), name='profile'),
    path('users/all/', ModeratorListView.as_view(), name='all_user'),
    path('user/<int:pk>/', ModeratorUpdateUserView.as_view(), name='detail_user'),
    path('user/<int:pk>/', delete_self_user, name='delete_user'),
]