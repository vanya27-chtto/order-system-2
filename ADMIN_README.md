# Каркас приложения админ-панели на Django

## Структура проекта

```
/workspace/
├── config/                 # Основной проект Django
│   ├── settings.py         # Настройки проекта
│   ├── urls.py             # Корневые URL
│   └── ...
├── admin_custom/           # Приложение кастомной админки
│   ├── models.py           # Модели (AdminUser, AdminRole, AdminPermission, AuditLog)
│   ├── admin.py            # Регистрация моделей в админке
│   ├── views.py            # Представления (дашборд, логин, логаут)
│   ├── utils.py            # Утилиты для логирования действий
│   ├── urls.py             # URL приложения
│   ├── templates/          # Шаблоны
│   │   └── admin_custom/
│   │       ├── admin_base.html    # Базовый шаблон админки
│   │       └── dashboard.html     # Страница дашборда
│   └── static/             # Статические файлы
│       └── admin_custom/
│           ├── css/admin_custom.css  # Стили
│           └── img/                  # Изображения
└── manage.py
```

## Возможности

### Модели
- **AdminUser** - кастомная модель пользователя с ролями и разрешениями
- **AdminRole** - роли администраторов (Суперадмин, Менеджер, Модератор и т.д.)
- **AdminPermission** - гибкая система разрешений
- **AuditLog** - журнал аудита всех действий администраторов

### Функционал
- Кастомный дашборд с быстрыми действиями
- Журнал аудита действий (создание, обновление, удаление, вход/выход)
- Система ролей и разрешений
- Логирование IP-адресов
- Красивый современный UI с градиентами

## Запуск

1. Применить миграции:
```bash
python manage.py migrate
```

2. Создать суперпользователя:
```bash
python manage.py createsuperuser
```

3. Запустить сервер разработки:
```bash
python manage.py runserver 0.0.0.0:8000
```

4. Открыть в браузере:
- Админка: http://localhost:8000/admin/
- Дашборд: http://localhost:8000/admin/dashboard/

## Данные для входа

- **Логин:** admin
- **Пароль:** admin123

## Настройка

### Добавление новой роли
```python
from admin_custom.models import AdminRole

role = AdminRole.objects.create(
    name='Менеджер',
    description='Управление контентом'
)
```

### Назначение роли пользователю
```python
from admin_custom.models import AdminUser, AdminRole

user = AdminUser.objects.get(username='admin')
user.role = AdminRole.objects.get(name='Менеджер')
user.save()
```

### Логирование действий
Автоматически логируются:
- Вход/выход из системы
- Просмотр страниц админки
- Создание, обновление, удаление объектов

## Расширение

Для добавления новых моделей в админку:

1. Создайте модель в `models.py` другого приложения
2. Зарегистрируйте в `admin.py`:
```python
from django.contrib import admin
from .models import YourModel

@admin.register(YourModel)
class YourModelAdmin(admin.ModelAdmin):
    list_display = ('field1', 'field2')
    search_fields = ('field1',)
```

## Технологии

- Django 6.0.5
- Python 3.12
- SQLite (база данных по умолчанию)
- Pillow (для работы с изображениями)
