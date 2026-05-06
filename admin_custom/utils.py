from .models import AuditLog


def log_admin_action(request, user, action, model_name, object_id='', changes=None, ip_address=None):
    """
    Функция для логирования действий администратора
    
    Args:
        request: Django request объект
        user: Пользователь, выполнивший действие
        action: Тип действия (CREATE, UPDATE, DELETE, LOGIN, LOGOUT, VIEW)
        model_name: Название модели
        object_id: ID объекта
        changes: Словарь с изменениями
        ip_address: IP адрес пользователя
    """
    if ip_address is None:
        ip_address = get_client_ip(request)
    
    if changes is None:
        changes = {}
    
    AuditLog.objects.create(
        admin_user=user,
        action=action,
        model_name=model_name,
        object_id=object_id,
        changes=changes,
        ip_address=ip_address,
    )


def get_client_ip(request):
    """Получение IP адреса клиента из запроса"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class AdminActionMiddleware:
    """
    Мидлварь для автоматического логирования действий администратора
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Логируем просмотр страниц админки
        if request.path.startswith('/admin/') and request.user.is_authenticated:
            # Извлекаем название модели из URL
            path_parts = request.path.strip('/').split('/')
            if len(path_parts) >= 3 and path_parts[0] == 'admin':
                model_name = path_parts[1] if len(path_parts) > 1 else 'Unknown'
                object_id = path_parts[3] if len(path_parts) > 3 else ''
                
                # Не логируем служебные страницы
                if model_name not in ['login', 'logout', 'password_change']:
                    log_admin_action(
                        request=request,
                        user=request.user,
                        action='VIEW',
                        model_name=model_name,
                        object_id=object_id,
                    )
        return None
