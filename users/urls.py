from django.urls import path
from users.views import UserCreateAPIView, UserListView, UserRetrieveView, UserUpdateView, \
    UserDeleteView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='user-create'),
    path('list/', UserListView.as_view(), name='user-list'),
    path('retrieve/', UserRetrieveView.as_view(), name='user-retrieve'),
    path('update/', UserUpdateView.as_view(), name='user-update'),
    path('destroy/', UserDeleteView.as_view(), name='user-destroy'),
    path('obtain/', TokenObtainPairView.as_view(), name='obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
]
