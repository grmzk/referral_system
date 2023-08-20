from django.contrib.auth.models import AbstractUser
from django.db import models

from referral_system.settings import INVITE_CODE_LENGTH

from .validators import (auth_code_regex_validator,
                         invite_code_regex_validator, username_regex_validator)


class User(AbstractUser):
    username = models.CharField(
        verbose_name='username',
        max_length=12,
        unique=True,
        blank=False,
        validators=[username_regex_validator],
    )
    invite_code = models.CharField(
        verbose_name='invite_code',
        max_length=INVITE_CODE_LENGTH,
        unique=True,
        blank=False,
        validators=[invite_code_regex_validator]
    )
    auth_code = models.CharField(
        verbose_name='auth_code',
        max_length=4,
        blank=True,
        null=True,
        validators=[auth_code_regex_validator],
    )
    referrer = models.ForeignKey(
        'self',
        verbose_name='referrer',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']

    def __str__(self):
        return f'{self.username}'
