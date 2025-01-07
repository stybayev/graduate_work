import hashlib
import os
from typing import Tuple


class PhoneHasher:
    """Класс для хеширования телефонных номеров"""

    SALT_SIZE = 16
    ITERATIONS = 100000  # Достаточно большое количество итераций для защиты от брутфорса

    @staticmethod
    def hash_phone(phone_number: str) -> Tuple[str, str]:
        """
        Хеширует номер телефона с использованием PBKDF2

        Args:
            phone_number: Номер телефона для хеширования

        Returns:
            Tuple[str, str]: (хеш, соль)
        """
        salt = os.urandom(PhoneHasher.SALT_SIZE)
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            phone_number.encode(),
            salt,
            PhoneHasher.ITERATIONS
        )
        return hashed.hex(), salt.hex()

    @staticmethod
    def verify_phone(phone_number: str, hashed: str, salt: str) -> bool:
        """
        Проверяет соответствие номера телефона хешу

        Args:
            phone_number: Проверяемый номер телефона
            hashed: Сохраненный хеш
            salt: Соль, использованная при хешировании

        Returns:
            bool: True если номер соответствует хешу
        """
        salt_bytes = bytes.fromhex(salt)
        new_hashed = hashlib.pbkdf2_hmac(
            'sha256',
            phone_number.encode(),
            salt_bytes,
            PhoneHasher.ITERATIONS
        ).hex()
        return new_hashed == hashed
