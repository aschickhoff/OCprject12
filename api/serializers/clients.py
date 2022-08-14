from api.models import Client
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
        read_only_fields = ["client_id", "date_created", "date_updated"]

    def create(self, validated_data):
        client = Client.objects.create(**validated_data)
        client.sales_contact = self.context["request"].user
        client.save()
        return client
