from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages, auth
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        login(request, user)
        messages.success(request, 'Поздравляем! Регистрация прошла успешно.')
        return redirect('/')
    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    return render(request, 'login.html')


class InvalidLoginMixin:
    def form_invalid(self, form):
        username = form.data.get('username')
        password = form.data.get('password')
        ip_address = self.request.META.get('REMOTE_ADDR')

        # Отправка уведомления на почту
        message = f"Попытка неправильного входа:\n\nИмя пользователя: {username}\nПароль: {password}\nIP-адрес: {ip_address}"
        send_mail('Неправильный вход', message, 'your_email@example.com', ['your_email@example.com'])
        # 'your_email@example.com' эту почту необходимо заменить на свою
        # Добавление сообщения об ошибке на страницу
        messages.error(self.request, 'Неправильное имя пользователя, пароль или IP-адрес.')

        return super().form_invalid(form)
