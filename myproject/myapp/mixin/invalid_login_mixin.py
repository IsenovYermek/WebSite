from django.core.mail import send_mail
from django.contrib import messages


class InvalidLoginMixin:
    def form_invalid(self, form):
        username = form.data.get('username')
        password = form.data.get('password')
        ip_address = self.request.META.get('REMOTE_ADDR')

        # Отправка уведомления по электронной почте
        message = f"Попытка неправильного входа:\n\nИмя пользователя: {username}\nПароль: {password}\nIP-адрес: {ip_address}"
        send_mail('Неправильный вход', message, 'your_email@example.com', ['your_email@example.com'])
        # вместо этого your_email@example.com можно написать свою почту
        # Добавление сообщения об ошибке на страницу
        messages.error(self.request, 'Неправильное имя пользователя, пароль или IP-адрес.')

        return super().form_invalid(form)