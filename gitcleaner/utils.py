"""
Утилиты для GitCleaner
"""

import os
import re
import fnmatch
from typing import List, Set, Union
from pathlib import Path

def human_readable_size(size_bytes: int) -> str:
    """Преобразует размер в байтах в человекочитаемый формат"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f}{size_names[i]}"

def parse_size(size_str: str) -> int:
    """Парсит строку размера в байты (например: '100MB', '1.5GB')"""
    size_str = size_str.strip().upper()
    
    # Регулярное выражение для парсинга размера
    match = re.match(r'^(\d+(?:\.\d+)?)\s*([KMGT]?B?)$', size_str)
    if not match:
        raise ValueError(f"Invalid size format: {size_str}")
    
    number = float(match.group(1))
    unit = match.group(2)
    
    multipliers = {
        'B': 1,
        'KB': 1024,
        'MB': 1024**2,
        'GB': 1024**3,
        'TB': 1024**4,
    }
    
    # Если единица измерения не указана, считаем байтами
    multiplier = multipliers.get(unit, 1) if unit else 1
    
    return int(number * multiplier)

def match_patterns(filename: str, patterns: List[str]) -> bool:
    """Проверяет, соответствует ли имя файла хотя бы одному паттерну"""
    for pattern in patterns:
        if fnmatch.fnmatch(filename, pattern):
            return True
        # Также проверяем полный путь
        if fnmatch.fnmatch(os.path.basename(filename), pattern):
            return True
    return False

def is_binary_file(data: bytes) -> bool:
    """Определяет, является ли файл бинарным"""
    # Проверяем первые 1024 байта
    chunk = data[:1024]
    
    # Если есть нулевые байты, скорее всего бинарный
    if b'\x00' in chunk:
        return True
    
    # Проверяем текстовые символы
    text_chars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
    return not all(c in text_chars for c in chunk)

def sanitize_filename(filename: str) -> str:
    """Очищает имя файла от недопустимых символов"""
    # Заменяем недопустимые символы
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename