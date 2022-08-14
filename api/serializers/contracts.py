from api.models import Contract
from rest_framework import serializers


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"
        read_only_fields = ["contract_id", "client", "date_created", "date_updated"]

    def create(self, validated_data):
        print(f" validated_data: {self.validated_data}")
        contract = Contract.objects.create(**validated_data)
        contract.sales_contact = self.context["request"].user
        # contract.client = self.context["request"].client
        contract.save()
        return contract
