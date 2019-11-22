from rest_framework import serializers
from src.board.models import Board


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('email', 'is_active', 'raw_content')
