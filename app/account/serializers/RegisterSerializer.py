from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
import re
from app.user.models import User
from app.account.serializers.UserSerializer import UserSerializer  # Import the correct serializer

password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,}$"


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True, max_length=128, write_only=True)
    password = serializers.CharField(required=True, max_length=128, write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=False,
                                   help_text=_("Role can be assigned only by an admin."))

    class Meta:
        model = User
        fields = ["id", "name", "username", "email", "password", "password2", "role"]
        extra_kwargs = {
            "email": {"required": True},
        }

    def validate_password(self, value):
        password = value
        password2 = self.initial_data.get("password2")
        if password != password2:
            raise serializers.ValidationError(_("Password fields didn't match"))

        password_check = re.match(password_pattern, value)
        if password_check is None:
            raise serializers.ValidationError(
                _(
                    "The password must be at least 6 characters long and contain at least one uppercase letter, "
                    "one lowercase letter, one digit, and one special character (#?!@$%^&*-)."
                )
            )
        return make_password(value)

    def validate(self, data):
        request = self.context.get("request")
        # Check if the user is an admin
        if request.user.is_staff:
            # Admin must explicitly specify a role (salesman or delivery)
            if 'role' not in data:
                raise ValidationError({
                    'role': _("Admin must specify a role (salesman or delivery) when creating staff accounts.")
                })
            if data['role'] == User.CUSTOMER:
                raise ValidationError(_("Admin cannot assign the 'customer' role."))
        else:
            # For non-admins, automatically assign the 'customer' role
            data['role'] = User.CUSTOMER

        return data

    def create(self, validated_data):
        # Remove password2 from validated_data since it's only used for validation
        validated_data.pop('password2', None)

        # Create the user with the validated data
        return User.objects.create(**validated_data)

    def to_representation(self, instance):
        """
        Use the UserSerializer to format the output of the user data.
        """
        return UserSerializer(instance).data
