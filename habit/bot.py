from users.models import User


def process_telegram_message(update):
    chat_id = update.message.chat.id
    text = update.message.text.strip()
    username = update.message.from_user.username

    if text.startswith("/start"):
        parts = text.split()
        if len(parts) == 2:
            try:
                user_id = int(parts[1])
                user = User.objects.get(id=user_id, telegram_username=username)
                user.telegram_chat_id = chat_id
                user.save()
                return "✅ Ваш аккаунт успешно привязан!"
            except (ValueError, User.DoesNotExist):
                return "❌ Неверный код привязки"
        return "👋 Для привязки аккаунта используйте команду из приложения"

    return "ℹ️ Отправьте /start для привязки аккаунта"
