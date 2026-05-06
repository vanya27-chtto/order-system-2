from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import AuditLog
from .utils import log_admin_action


@staff_member_required
def dashboard(request):
    """Кастомная страница дашборда администратора"""
    # Получаем статистику
    recent_logs = AuditLog.objects.select_related('admin_user').order_by('-timestamp')[:10]
    
    context = {
        'recent_logs': recent_logs,
        'title': 'Панель управления',
    }
    return render(request, 'admin_custom/dashboard.html', context)


class CustomAdminLoginView(LoginView):
    """Кастомная страница входа"""
    template_name = 'admin_custom/login.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Логируем вход
        log_admin_action(
            request=self.request,
            user=self.request.user,
            action='LOGIN',
            model_name='User',
        )
        return response


class CustomAdminLogoutView(LogoutView):
    """Кастомная страница выхода"""
    
    def dispatch(self, request, *args, **kwargs):
        # Логируем выход
        if request.user.is_authenticated:
            log_admin_action(
                request=request,
                user=request.user,
                action='LOGOUT',
                model_name='User',
            )
        return super().dispatch(request, *args, **kwargs)
