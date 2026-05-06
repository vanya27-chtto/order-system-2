from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class AdminRole(models.Model):
    """Модель ролей администраторов"""
    name = models.CharField(_('Название роли'), max_length=50, unique=True)
    description = models.TextField(_('Описание'), blank=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    class Meta:
        verbose_name = _('Роль')
        verbose_name_plural = _('Роли')
        ordering = ['name']

    def __str__(self):
        return self.name


class AdminPermission(models.Model):
    """Модель разрешений для администраторов"""
    name = models.CharField(_('Название разрешения'), max_length=100)
    codename = models.CharField(_('Код разрешения'), max_length=50, unique=True)
    description = models.TextField(_('Описание'), blank=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    class Meta:
        verbose_name = _('Разрешение')
        verbose_name_plural = _('Разрешения')
        ordering = ['codename']

    def __str__(self):
        return f"{self.name} ({self.codename})"


class AdminUser(AbstractUser):
    """Модель пользователя админ-панели"""
    role = models.ForeignKey(
        AdminRole, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='admins',
        verbose_name=_('Роль')
    )
    permissions = models.ManyToManyField(
        AdminPermission,
        blank=True,
        related_name='admins',
        verbose_name=_('Разрешения')
    )
    phone = models.CharField(_('Телефон'), max_length=20, blank=True)
    avatar = models.ImageField(_('Аватар'), upload_to='admin_avatars/', null=True, blank=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    class Meta:
        verbose_name = _('Администратор')
        verbose_name_plural = _('Администраторы')
        ordering = ['-created_at']

    def __str__(self):
        return self.username


class AuditLog(models.Model):
    """Модель аудита действий администраторов"""
    ACTION_CHOICES = [
        ('CREATE', 'Создание'),
        ('UPDATE', 'Обновление'),
        ('DELETE', 'Удаление'),
        ('LOGIN', 'Вход в систему'),
        ('LOGOUT', 'Выход из системы'),
        ('VIEW', 'Просмотр'),
    ]

    admin_user = models.ForeignKey(
        AdminUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs',
        verbose_name=_('Администратор')
    )
    action = models.CharField(_('Действие'), max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(_('Модель'), max_length=100)
    object_id = models.CharField(_('ID объекта'), max_length=50, blank=True)
    changes = models.JSONField(_('Изменения'), default=dict, blank=True)
    ip_address = models.GenericIPAddressField(_('IP адрес'), null=True, blank=True)
    timestamp = models.DateTimeField(_('Время'), auto_now_add=True)

    class Meta:
        verbose_name = _('Журнал аудита')
        verbose_name_plural = _('Журналы аудита')
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.admin_user.username if self.admin_user else 'Unknown'} - {self.action} - {self.model_name}"
