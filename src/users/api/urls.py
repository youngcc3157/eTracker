from django.urls import path, include

from .views import UserDetailView, UserListView

urlpatterns = [
    path('', UserListView.as_view()),
    path('<pk>', UserDetailView.as_view()),
]
