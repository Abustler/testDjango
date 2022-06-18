from django.urls import path, re_path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'
urlpatterns = [
    # re_path(r'^login/$', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('account:password_change_done')), name='password_change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('account:password_reset_done')), name='password_reset'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('account:password_reset_complete')), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('my-information/', views.myself, name='my_information'),
    path('edit-my-information', views.myself_edit, name='edit_my_information'),
    path('my-image/', views.my_image, name='my_image')
]