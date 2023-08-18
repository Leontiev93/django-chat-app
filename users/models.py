from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from django.core.validators import RegexValidator

from users.validators import FirstLastnameValidator


class User(AbstractUser):
    """Модель пользователя"""
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=settings.LENGTH_USER,
        unique=True,
        validators=(UnicodeUsernameValidator(),
                    RegexValidator(
                        regex=r'\b(ME|me|Me|mE)\b',
                        message='Нельзя использовать имя me,Me,mE,ME',
                        code='invalid',
                        inverse_match=True,
        )),
        help_text=(
            'Требуется. Не более 150 символов. Только буквы, цифры и @/./+/-/_'
        ),
        error_messages={
            'unique': 'Пользователь с таким именем уже существует',
        },
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.LENGTH_USER,
        validators=(FirstLastnameValidator(),),
        help_text=('Введите свое имя'),
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.LENGTH_USER,
        validators=(FirstLastnameValidator(),),
        help_text=('Введите свою фамилию'),
    )
    email = models.EmailField(
        verbose_name='email адрес',
        max_length=settings.LENGTH_USER_EMAIL,
        unique=True,
        help_text=(
            'Введите электронный адрес в формате name@yandex.ru'
        ),
    )
    password = models.CharField(
        max_length=settings.LENGTH_USER,
        verbose_name='Пароль',
        help_text='Придумайте пароль'
    )
    contractor = models.ManyToManyField(
        'self',
        through='Contract',
        related_name='contractors',
        symmetrical=False
    )

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('username', 'email')
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username


class Contract(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customer',
        verbose_name='Заказчик',
        help_text='Заказчик работ',
    )
    contractor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='to_contractor',
        verbose_name='Исполнитель',
        help_text='Исполнитель работ',
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=(
                'customer', 'contractor'), name='unique_contract'),
            models.CheckConstraint(
                check=~models.Q(customer=models.F(
                 'contractor')),
                name="you_can't_make_a_contract_with_yourself"),
        ]
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.customer} договорился о сделке с {self.contractor}'
