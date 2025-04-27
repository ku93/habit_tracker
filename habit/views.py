import telegram
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from habit.models import Habit
from habit.pagination import HabitPagination
from habit.serializers import HabitSerializer, PublicHabitSerializer
from habit_tracker.settings import TELEGRAM_BOT_TOKEN
from users.models import User


class HabitViewSet(ModelViewSet):
    '''CRUD операции для привычек текущего пользователя'''
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PublicHabitViewSet(ReadOnlyModelViewSet):
    '''операции для публичных привычек'''
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = PublicHabitSerializer
    pagination_class = HabitPagination
    permission_classes = [AllowAny]


class TelegramConnectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        telegram_username = request.data.get('telegram_username')

        if not telegram_username:
            return Response(
                {'error': 'Требуется telegram_username'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(telegram_username=telegram_username).exclude(id=user.id).exists():
            return Response(
                {'error': 'Этот Telegram уже привязан к другому аккаунту'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.telegram_username = telegram_username
        user.save()

        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        try:
            bot.send_message(
                chat_id=telegram_username,
                text=f"Для завершения привязки отправьте боту команду: /start {user.id}"
            )
            return Response(
                {'status': 'Инструкция отправлена в Telegram'},
                status=status.HTTP_200_OK
            )
        except telegram.error.TelegramError as e:
            return Response(
                {'error': f'Ошибка Telegram: {e}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class TelegramWebhookView(APIView):
    def post(self, request):
        from .bot import process_telegram_message
        update = telegram.Update.de_json(request.data, telegram.Bot(TELEGRAM_BOT_TOKEN))
        if update.message:
            response = process_telegram_message(update)
            bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
            bot.send_message(
                chat_id=update.message.chat.id,
                text=response
            )
        return Response(status=status.HTTP_200_OK)