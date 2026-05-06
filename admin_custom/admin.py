from django.contrib import admin

# Register your models here.
from .models import AdminUser, AdminRole, AdminPermission, AuditLog

@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('-created_at',)

@admin.register(AdminRole)
class AdminRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)

@admin.register(AdminPermission)
class AdminPermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'codename')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('admin_user', 'action', 'model_name', 'object_id', 'timestamp')
    list_filter = ('action', 'model_name', 'timestamp')
    search_fields = ('admin_user__username', 'model_name', 'object_id')
    readonly_fields = ('admin_user', 'action', 'model_name', 'object_id', 'changes', 'ip_address', 'timestamp')
    ordering = ('-timestamp',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
