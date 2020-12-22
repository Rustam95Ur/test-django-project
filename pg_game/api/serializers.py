from rest_framework import serializers
from histories.models import AgentImage


class AgentImageSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализация картинки для обновления профиля"""
    code = serializers.CharField()
    image = serializers.ImageField()

    class Meta:
        model = AgentImage
        fields = ('code', 'image',)
