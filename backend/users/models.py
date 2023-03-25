from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser, \
    _user_has_perm, _user_has_module_perms
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Кастомный менеджер объектов модели User."""

    def create_user(self, email, username, role=None, password=None, **others):
        if not email:
            raise ValueError(_("У пользователя должен быть указан email"))
        if role is None:
            role = User.USER

        validate_password(password)

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            role=role,
            **others
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **others):
        user = self.model(email=self.normalize_email(email), username=username)
        user.is_superuser = True
        user.is_staff = True
        user.role = User.ADMIN
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователей."""

    USER = "user"
    ADMIN = "admin"
    ROLE_CHOICES = [
        (USER, "Пользователь"),
        (ADMIN, "Администратор"),
    ]

    username_validator = UnicodeUsernameValidator()

    password = models.CharField(
        _("Пароль"),
        max_length=128,
        error_messages=_("Введен некорретный пароль"),
    )
    username = models.CharField(
        _("Юзернейм"),
        max_length=150,
        unique=True,
        help_text=_(
            "Обязательное поле. Не более 150 символов. "
            "Допустимые символы: буквы, цифры и @/./+/-/_."
        ),
        validators=(username_validator,),
        error_messages={
            "unique": _("Пользователь с таким имененем уже существует."),
        },
    )
    email = models.EmailField(_("Почта"), max_length=254, unique=True)
    first_name = models.CharField(_("Имя"), max_length=150)
    last_name = models.CharField(_("Фамилия"), max_length=150)
    role = models.CharField(
        _("Статус пользователя"),
        max_length=128,
        choices=ROLE_CHOICES,
        default=USER,
        help_text=(
            "Выберите статус пользователя. Дефолт - user. "
            "От выбора зависят его права."
        ),
    )
    is_active = models.BooleanField(
        _("Активный/неактивный."),
        default=True,
        help_text=_("Статус текущего аккаунта - активирован или нет."),
    )
    is_staff = models.BooleanField(
        _("Статус служебного персонала"),
        default=False,
        help_text=_("Является ли пользователь суперюзером."),
    )
    is_blocked = models.BooleanField(
        _("Статус блокировки пользователя"),
        default=False,
        help_text=_("Заблокирован ли пользователь."),
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff or self.is_superuser

    def has_module_perms(self, app_label):
        if self.is_active and self.is_admin:
            return True
        return super().has_module_perms(app_label)

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_admin:
            return True
        return super().has_perm(perm, obj)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name")
    objects = UserManager()

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        ordering = ("username",)

    def __str__(self):
        return self.username[:50]


class Subscription(models.Model):
    """Модель подписок."""

    user = models.ForeignKey(
        User,
        verbose_name=_("Текущий пользователь"),
        related_name="subscriber",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        verbose_name=_("На кого подписан текущий пользователь"),
        related_name="subscribe_object",
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("user", "author"), name="unique subscription"
            ),
        )
