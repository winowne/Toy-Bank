"""Business logic for the small console bank."""

from __future__ import annotations

import copy
import hashlib
import hmac
import secrets
from datetime import datetime, timezone
from typing import Any

from src.storage import HISTORY_FILE, USERS_FILE, load_json, save_json


class BankError(Exception):
    """Expected error that can be shown to a bank customer."""


class Bank:
    def __init__(self) -> None:
        raw_users = load_json(USERS_FILE, {})
        if not isinstance(raw_users, dict):
            raise ValueError("Файл пользователей должен содержать объект JSON")
        self.users: dict[str, dict[str, Any]] = {}
        self._migrate_users(raw_users)
        raw_history = load_json(HISTORY_FILE, [])
        if not isinstance(raw_history, list):
            raise ValueError("Файл истории должен содержать список JSON")
        self.history: list[dict[str, Any]] = raw_history

    def _migrate_users(self, raw_users: dict[str, dict[str, Any]]) -> None:
        changed = False
        usernames: set[str] = set()
        for user_id, user in raw_users.items():
            if not isinstance(user, dict):
                raise ValueError(f"Некорректные данные пользователя {user_id}")
            if "username" not in user or "balance" not in user:
                raise ValueError(f"У пользователя {user_id} не хватает данных")
            user = dict(user)
            username_key = str(user["username"]).strip().casefold()
            if not username_key or username_key in usernames:
                raise ValueError("Имена пользователей должны быть непустыми и уникальными")
            usernames.add(username_key)
            if user.get("user_id") != user_id:
                user["user_id"] = user_id
                changed = True
            if "pin_hash" not in user:
                if "pin" not in user:
                    raise ValueError(f"У пользователя {user_id} не задан PIN")
                user["pin_hash"] = self._hash_pin(str(user.pop("pin")))
                changed = True
            user["balance"] = int(user["balance"])
            if user["balance"] < 0:
                raise ValueError(f"Баланс пользователя {user_id} не может быть отрицательным")
            self.users[user_id] = user
        if changed:
            self._save_users()

    @staticmethod
    def _hash_pin(pin: str, salt: str | None = None) -> str:
        salt = salt or secrets.token_hex(16)
        digest = hashlib.pbkdf2_hmac("sha256", pin.encode(), salt.encode(), 120_000)
        return f"{salt}${digest.hex()}"

    @classmethod
    def _pin_matches(cls, pin: str, stored_hash: str) -> bool:
        try:
            salt, expected = stored_hash.split("$", 1)
        except ValueError:
            return False
        actual = cls._hash_pin(pin, salt).split("$", 1)[1]
        return hmac.compare_digest(actual, expected)

    def authenticate(self, pin: str) -> dict[str, Any] | None:
        for user in self.users.values():
            if self._pin_matches(pin, str(user["pin_hash"])):
                return user
        return None

    def find_user(self, username: str) -> dict[str, Any] | None:
        normalized = username.casefold()
        return next(
            (user for user in self.users.values() if str(user["username"]).casefold() == normalized),
            None,
        )

    def transfer(self, sender: dict[str, Any], recipient_name: str, amount: int) -> dict[str, Any]:
        recipient = self.find_user(recipient_name)
        if recipient is None:
            raise BankError("Такого пользователя не существует")
        if recipient is sender:
            raise BankError("Нельзя переводить деньги самому себе")
        self._validate_amount(amount)
        if amount > sender["balance"]:
            raise BankError("Недостаточно средств")

        sender["balance"] -= amount
        recipient["balance"] += amount
        return self._commit(
            {"type": "transfer", "sender": sender["username"],
             "recipient": recipient["username"], "amount": amount}
        )

    def deposit(self, user: dict[str, Any], amount: int) -> dict[str, Any]:
        self._validate_amount(amount)
        user["balance"] += amount
        return self._commit({"type": "deposit", "recipient": user["username"], "amount": amount})

    def withdraw(self, user: dict[str, Any], amount: int) -> dict[str, Any]:
        self._validate_amount(amount)
        if amount > user["balance"]:
            raise BankError("Недостаточно средств")
        user["balance"] -= amount
        return self._commit({"type": "withdraw", "sender": user["username"], "amount": amount})

    def change_pin(self, user: dict[str, Any], old_pin: str, new_pin: str) -> None:
        if not self._pin_matches(old_pin, str(user["pin_hash"])):
            raise BankError("Текущий PIN-код указан неверно")
        if not new_pin.isdigit() or len(new_pin) != 4 or new_pin == "0000":
            raise BankError("Новый PIN должен состоять из четырех цифр и не быть 0000")
        old_hash = user["pin_hash"]
        user["pin_hash"] = self._hash_pin(new_pin)
        try:
            self._save_users()
        except OSError as error:
            user["pin_hash"] = old_hash
            raise BankError("Не удалось сохранить новый PIN-код") from error

    @staticmethod
    def _validate_amount(amount: int) -> None:
        if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
            raise BankError("Сумма должна быть положительным целым числом")

    def _commit(self, details: dict[str, Any]) -> dict[str, Any]:
        users_before = copy.deepcopy(self.users)
        history_before = copy.deepcopy(self.history)
        operation = {
            "id": secrets.token_hex(6),
            "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            **details,
        }
        self.history.append(operation)
        try:
            self._save_users()
            save_json(HISTORY_FILE, self.history)
        except OSError as error:
            self.users = users_before
            self.history = history_before
            try:
                self._save_users()
                save_json(HISTORY_FILE, self.history)
            except OSError:
                pass
            raise BankError("Не удалось сохранить операцию") from error
        return operation

    def user_history(self, username: str) -> list[dict[str, Any]]:
        normalized = username.casefold()
        return [
            operation
            for operation in self.history
            if operation.get("sender", "").casefold() == normalized
            or operation.get("recipient", "").casefold() == normalized
        ]

    def _save_users(self) -> None:
        save_json(USERS_FILE, self.users)
