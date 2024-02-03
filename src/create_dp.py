from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage = MemoryStorage()

dp = Dispatcher(storage=storage)
