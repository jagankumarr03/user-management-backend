from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import admin_users_api, toggle_user_status_api

from .views import (
    signup,
    login_view,
    dashboard,
    logout_view,
    edit_profile,
    admin_dashboard,
    user_profile_api,
    update_profile_api,
    change_password_api,
    api_signup,
)

urlpatterns = [
    # HTML views
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('logout/', logout_view, name='logout'),
    path('api/admin/users/', admin_users_api),
    path('api/admin/users/<int:user_id>/toggle/', toggle_user_status_api),
    path('api/signup/', api_signup),



    # Password change (HTML)
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/password_change.html',
            success_url='/password-change-done/'
        ),
        name='password_change'
    ),
    path(
        'password-change-done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/password_change_done.html'
        ),
        name='password_change_done'
    ),

    # API endpoints (React)
    path('api/profile/', user_profile_api),
    path('api/profile/update/', update_profile_api),
    path('api/change-password/', change_password_api),

    # JWT
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]
