from rest_framework import serializers
from .models import Task, File

class TaskSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=255)
    id_image = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Tasks.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.id_image = validated_data.get('id_image', instance.id_image)
        instance.save()
        return instance

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"
