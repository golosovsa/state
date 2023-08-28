from abc import ABC
from pathlib import Path
from typing import Dict, Any


class BaseStorage(ABC):
    """Абстрактное хранилище состояния.

    Позволяет сохранять и получать состояние.
    Способ хранения состояния может варьироваться в зависимости
    от итоговой реализации. Например, можно хранить информацию
    в базе данных или в распределённом файловом хранилище.
    """

    @abc.abstractmethod
    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""

    @abc.abstractmethod
    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""


class JsonFileStorage(BaseStorage):
    """Реализация хранилища, использующего локальный файл.

    Формат хранения: JSON
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path).resolve()
        if not self.file_path.exists():
            self.save_state({})

    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""
        with self.file_path.open('wt', encoding='utf-8') as file:
            json.dump(state, file)

    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""
        with self.file_path.open('rt', encoding='utf-8') as file:
            return json.load(file)


class RedisStorage(BaseStorage):
    def __init__(self, redis):
        self.redis = redis
        if self.redis.get('state') is None:
            self.redis.set('state', {})

    def save_state(self, state: Dict[str, Any]) -> None:
        self.redis.set('state', state)

    def retrieve_state(self) -> Dict[str, Any]:
        return self.redis.get('state')
