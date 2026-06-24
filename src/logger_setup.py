"""
logger_setup.py - Настройка логирования для системы управления школой
"""

import logging
import os
from datetime import datetime


def setup_logger():
    """
    Настраивает логирование для приложения.
    
    Returns:
        logging.Logger: Настроенный логгер
    """
    
    # Создаём папку для логов, если её нет
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Создаём логгер
    logger = logging.getLogger('school')
    logger.setLevel(logging.DEBUG)
    
    # Очищаем существующие обработчики (чтобы избежать дублирования)
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 1. Обработчик для файла (все уровни)
    log_file = f"{log_dir}/school.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 2. Обработчик для консоли (только INFO и выше)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 3. Обработчик для ошибок (отдельный файл)
    error_file = f"{log_dir}/errors.log"
    error_handler = logging.FileHandler(error_file, encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    return logger


# Создаём экземпляр логгера для использования в других модулях
logger = setup_logger()


# Функция для логирования действий пользователя
def log_user_action(action: str, user: str = None, details: str = None):
    """
    Логирует действие пользователя.
    
    Args:
        action: Действие (например, "add_student", "enroll_course")
        user: Имя пользователя (опционально)
        details: Дополнительные детали (опционально)
    """
    msg = f"Действие: {action}"
    if user:
        msg += f" | Пользователь: {user}"
    if details:
        msg += f" | {details}"
    
    logger.info(msg)


# Функция для логирования ошибок
def log_error(error: Exception, context: str = None):
    """
    Логирует ошибку с контекстом.
    
    Args:
        error: Объект исключения
        context: Контекст, в котором произошла ошибка
    """
    msg = f"ОШИБКА: {type(error).__name__}: {error}"
    if context:
        msg = f"[{context}] {msg}"
    
    logger.error(msg)
    # Также логируем traceback для отладки
    import traceback
    logger.debug(traceback.format_exc())


# Тестовый запуск
if __name__ == "__main__":
    # Проверка работы логгера
    print("🔍 Проверка логирования...")
    
    logger.info("Тестовое информационное сообщение")
    logger.warning("Тестовое предупреждение")
    logger.error("Тестовая ошибка")
    
    log_user_action("test_action", "admin", "Тестовое действие")
    
    try:
        raise ValueError("Тестовая ошибка")
    except Exception as e:
        log_error(e, "Тестовый контекст")
    
    print("✅ Логирование работает. Проверьте папку logs/")
