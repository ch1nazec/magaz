from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Админка для кастомной модели пользователя"""
    
    # Поля, отображаемые в списке пользователей
    list_display = [
        'username', 'phone_number', 'email', 'telegram_id',
        'address', 'is_staff', 'is_active'
    ]
    
    # Поля для фильтрации
    list_filter = ['is_staff', 'is_active', 'is_superuser']
    
    # Поля для поиска
    search_fields = ['username', 'email', 'phone_number']
    
    # Поля для редактирования в списке
    list_editable = ['phone_number', 'address']
    
    # Поля, которые можно читать, но не редактировать
    readonly_fields = ['last_login', 'date_joined']
    
    # Поля для формы добавления пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'phone_number', 'address',
                'password1', 'password2',
            ),
        }),
    )
    
    # Поля для формы редактирования
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'email',
                'phone_number', 'address', 'telegram_id'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            ),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    # Поля, используемые при создании пользователя
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
    
    def save_model(self, request, obj, form, change):
        """Хэширование пароля при сохранении"""
        if not change:  # Новый пользователь
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)