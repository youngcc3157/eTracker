from rest_framework.generics import ListAPIView, RetrieveAPIView
from src.board.models import Board
from .serializers import BoardSerializer


class BoardListView(ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class BoardDetailView(RetrieveAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
