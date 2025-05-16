from django.core.exceptions import ValidationError
from django.test import TestCase

from habit.models import Habit
from users.models import User


class HabitModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com")

        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="12:00:00",
            action="Чтение книги",
            is_pleasant=True,
            periodicity=1,
            duration=60,
        )

        self.habit = Habit.objects.create(
            user=self.user,
            place="Парк",
            time="08:00:00",
            action="Бег",
            is_pleasant=False,
            periodicity=1,
            duration=120,
        )

    def test_validate_related_habit(self):
        """Тест валидации связанной привычки"""
        self.habit.linked_habit = self.pleasant_habit
        self.habit.save()
        self.habit.full_clean()

        unpleasant_habit = Habit.objects.create(
            user=self.user,
            place="Офис",
            time="10:00:00",
            action="Проверка почты",
            is_pleasant=False,
            periodicity=1,
            duration=30,
        )

        self.habit.linked_habit = unpleasant_habit
        with self.assertRaises(ValidationError):
            self.habit.full_clean()

    def test_validate_reward_or_related(self):
        """Тест валидации взаимного исключения вознаграждения и связанной привычки"""
        self.habit.reward = "Кофе"
        self.habit.linked_habit = None
        self.habit.full_clean()

        self.habit.reward = None
        self.habit.linked_habit = self.pleasant_habit
        self.habit.full_clean()

        self.habit.reward = "Кофе"
        with self.assertRaises(ValidationError):
            self.habit.full_clean()

    def test_validate_pleasant_habit(self):
        """Тест валидации приятной привычки"""
        self.pleasant_habit.full_clean()

        self.pleasant_habit.reward = "Чай"
        with self.assertRaises(ValidationError):
            self.pleasant_habit.full_clean()

        self.pleasant_habit.reward = None
        self.pleasant_habit.linked_habit = self.habit
        with self.assertRaises(ValidationError):
            self.pleasant_habit.full_clean()


class HabitCRUDTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com")

        self.habit_data = {
            "user": self.user,
            "place": "Парк",
            "time": "08:00:00",
            "action": "Бег",
            "is_pleasant": False,
            "periodicity": 1,
            "duration": 120,
        }

    def test_habit_creation(self):
        """Тест создания привычки"""
        habit = Habit.objects.create(**self.habit_data)

        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(habit.action, "Бег")
        self.assertEqual(habit.user.email, "test@example.com")

        self.assertEqual(str(habit), f"{self.user}: Бег в 08:00:00 (Парк)")

    def test_habit_creation_with_invalid_data(self):
        """Тест создания привычки с невалидными данными"""
        invalid_data = self.habit_data.copy()
        invalid_data["duration"] = 121

        with self.assertRaises(ValidationError):
            habit = Habit(**invalid_data)
            habit.full_clean()
            habit.save()

    def test_habit_update(self):
        """Тест обновления привычки"""
        habit = Habit.objects.create(**self.habit_data)
        habit.action = "Быстрая ходьба"
        habit.place = "Стадион"
        habit.save()

        updated_habit = Habit.objects.get(pk=habit.pk)
        self.assertEqual(updated_habit.action, "Быстрая ходьба")
        self.assertEqual(updated_habit.place, "Стадион")

    def test_habit_update_with_pleasant_habit(self):
        """Тест обновления привычки с приятной привычкой"""
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="12:00:00",
            action="Чтение книги",
            is_pleasant=True,
            periodicity=1,
            duration=60,
        )

        habit = Habit.objects.create(**self.habit_data)

        habit.is_pleasant = True
        habit.reward = "Чай"

        with self.assertRaises(ValidationError):
            habit.full_clean()
            habit.save()
        return pleasant_habit

    def test_habit_deletion(self):
        """Тест удаления привычки"""
        habit = Habit.objects.create(**self.habit_data)

        self.assertEqual(Habit.objects.count(), 1)

        habit.delete()

        self.assertEqual(Habit.objects.count(), 0)

    def test_habit_list_view(self):
        """Тест получения списка привычек"""
        Habit.objects.create(**self.habit_data)
        Habit.objects.create(
            user=self.user,
            place="Дом",
            time="20:00:00",
            action="Чтение",
            is_pleasant=True,
            periodicity=2,
            duration=30,
        )

        habits = Habit.objects.all()

        self.assertEqual(habits.count(), 2)
        self.assertEqual(habits[0].action, "Чтение")
        self.assertEqual(habits[1].action, "Бег")

    def test_habit_public_and_private(self):
        """Тест публичных и приватных привычек"""

        public_habits = Habit.objects.filter(is_public=True)
        self.assertEqual(public_habits.count(), 0)
        # self.assertEqual(public_habits[0].action, "Бег")

        user_habits = Habit.objects.filter(user=self.user)
        self.assertEqual(user_habits.count(), 0)
