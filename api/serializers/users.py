from api.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "position",
            "password",
            "is_staff",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


# class RegisterUserSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

#     class Meta:
#         model = User
#         fields = [
#             "id",
#             "username",
#             "first_name",
#             "last_name",
#             "email",
#             "password",
#             "password2",
#             "position",
#         ]
#         extra_kwargs = {"password": {"write_only": True}}

#     def save(self):
#         password = self.validated_data["password"]
#         password2 = self.validated_data["password2"]

#         if password != password2:
#             raise serializers.ValidationError({"error": "Password mismatch"})

#         if User.objects.filter(email=self.validated_data["email"]).exists():
#             raise serializers.ValidationError({"error": "Email already exists"})

#         account = User(
#             username=self.validated_data["username"],
#             first_name=self.validated_data["first_name"],
#             last_name=self.validated_data["last_name"],
#             email=self.validated_data["email"],
#             position=self.validated_data["position"],
#         )
#         account.set_password(password)
#         account.save()

#         return account
