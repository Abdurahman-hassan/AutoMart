from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from typing import ClassVar
from .managers import UserManager


class User(AbstractUser):
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=False, max_length=90)
    email = models.EmailField(
        _("Email Address"),
        blank=False,
        unique=True,
    )
    email_verified = models.BooleanField(_("Email Verified"), default=False)
    avatar = models.ImageField(_("Avatar"), default="avatar.svg", upload_to="avatar/")

    # Define role choices
    CUSTOMER = 'customer'
    SALESMAN = 'salesman'
    DELIVERY = 'delivery'
    ROLE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (SALESMAN, 'Salesman'),
        (DELIVERY, 'Delivery'),
    ]
    role = models.CharField(
        _("User Role"),
        max_length=50,
        choices=ROLE_CHOICES,
        default=CUSTOMER,
        blank=True,
        null=True,
        db_index=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    class Meta:
        ordering = ["-email"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["role"]),
        ]

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = None
        super().save(*args, **kwargs)
