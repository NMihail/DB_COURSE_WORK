from django.http import HttpResponseForbidden
from functools import wraps

# Декоратор для проверки роли пользователя
def role_required(required_role):
    """
    Декоратор для проверки роли пользователя.
    :param required_role: Роль, которая необходима для доступа
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Проверка роли пользователя
            user_role = 'none'
            try:
                user_role = request.session.get('role')
            except Exception as e:
                pass

            if user_role != required_role:
                return HttpResponseForbidden("У вас нет прав для доступа к этой странице")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator