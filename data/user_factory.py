"""
Фабрика тестовых данных для пользователей.
Позволяет генерировать случайные данные для тестирования API пользователей.
"""

from typing import Dict, List

from faker import Faker


class UserFactory:
    """Фабрика для генерации тестовых данных пользователей."""

    def __init__(self, locale: str = 'ru_RU'):
        self.fake = Faker(locale)

    def generate_single_user_data(
            self,
            include_optional_fields: bool = True,
            **overrides
    ) -> Dict[str, any]:
        """
        Генерирует данные для одного пользователя.

        Args:
            include_optional_fields: Включать ли опциональные поля
            **overrides: Переопределение конкретных полей

        Returns:
            Словарь с данными пользователя
        """
        user_data = {
            "name": self.fake.name(),
            "email": self.fake.email(),
        }

        if include_optional_fields:
            user_data.update({
                "phone": self.fake.phone_number(),
                "address": self.fake.address(),
                "birth_date": str(self.fake.date_of_birth()),
            })

        # Применяем переопределения
        user_data.update(overrides)

        return user_data

    def generate_multiple_users_data(
            self,
            count: int = 1,
            include_optional_fields: bool = True,
            **overrides
    ) -> List[Dict[str, any]]:
        """
        Генерирует данные для нескольких пользователей.

        Args:
            count: Количество пользователей для генерации
            include_optional_fields: Включать ли опциональные поля
            **overrides: Переопределение конкретных полей для всех пользователей

        Returns:
            Список словарей с данными пользователей
        """
        return [
            self.generate_single_user_data(
                include_optional_fields=include_optional_fields,
                **overrides
            )
            for _ in range(count)
        ]

    def generate_user_with_required_only(self) -> Dict[str, any]:
        """
        Генерирует данные пользователя только с обязательными полями.

        Returns:
            Словарь с данными пользователя (только обязательные поля)
        """
        return self.generate_single_user_data(include_optional_fields=False)

    def generate_user_with_custom_email(self, email: str) -> Dict[str, any]:
        """
        Генерирует данные пользователя с заданным email.

        Args:
            email: Конкретный email для пользователя

        Returns:
            Словарь с данными пользователя
        """
        return self.generate_single_user_data(email=email)


# Создаем экземпляр фабрики по умолчанию для удобства
user_factory = UserFactory()


# Функции для быстрого доступа

def get_single_user(include_optional_fields: bool = True, **overrides) -> Dict[
        str, any]:
    """Генерирует данные одного пользователя."""
    return user_factory.generate_single_user_data(
        include_optional_fields=include_optional_fields,
        **overrides
    )


def get_multiple_users(count: int = 1, include_optional_fields: bool = True,
                       **overrides) -> List[Dict[str, any]]:
    """Генерирует данные нескольких пользователей."""
    return user_factory.generate_multiple_users_data(
        count=count,
        include_optional_fields=include_optional_fields,
        **overrides
    )


def get_user_required_only() -> Dict[str, any]:
    """Генерирует данные пользователя только с обязательными полями."""
    return user_factory.generate_user_with_required_only()


def get_user_with_email(email: str) -> Dict[str, any]:
    """Генерирует данные пользователя с конкретным email."""
    return user_factory.generate_user_with_custom_email(email)
