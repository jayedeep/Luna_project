from django.urls import path
from . views import SetNewPasswordAPIView,RequestPasswordResetEmail,ChangePasswordView,CustomUserCreate,CurrentUserWithPost, PasswordTokenCheckApi,ProfileShower,AllUsers,BlacklistTokenView,CustomTokenObtainPairView

urlpatterns = [
    path('api/token/',CustomTokenObtainPairView.as_view(),name='token_obtain_pair'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('register',CustomUserCreate.as_view(),name="register"),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),

    path('allusers',AllUsers.as_view(),name="alluser"),
    path('logout/blacklist/',BlacklistTokenView.as_view(),name='blacklist'),
    path('profile',CurrentUserWithPost.as_view(),name="profile"),
    path('userpost',ProfileShower.as_view(),name='userpost'),
    path('request-reset-email',RequestPasswordResetEmail.as_view(),name='request-reset-email'),
    path('password-reset/<uid64>/<token>',PasswordTokenCheckApi.as_view(),name='password-reset'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete')
]