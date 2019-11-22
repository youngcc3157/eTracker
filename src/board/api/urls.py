from django.urls import path, include

from .views import BoardDetailView, BoardListView

urlpatterns = [
    path('', BoardListView.as_view()),
    path('<pk>', BoardDetailView.as_view()),
]
