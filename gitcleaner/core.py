"""
Основной класс GitCleaner
"""

import os
import subprocess
import logging
from typing import List, Dict, Set, Optional, Callable
from pathlib import Path
from tqdm import tqdm

from .cleaner import Cleaner
from .exceptions import GitRepositoryError, GitCommandError
from .utils import parse_size, human_readable_size

class GitCleaner:
    """Основной класс для очистки Git репозитория"""
    
    def __init__(self, repo_path: str = ".", dry_run: bool = False):
        """
        Инициализация GitCleaner
        
        Args:
            repo_path: Путь к Git репозиторию
            dry_run: Режим "пробного" запуска (без изменений)
        """
        self.repo_path = Path(repo_path).resolve()
        self.dry_run = dry_run
        self.cleaner = Cleaner(repo_path, dry_run)
        
        # Настройка логгирования
        self.logger = logging.getLogger(__name__)
        
        # Проверка, что это Git репозиторий
        if not self._is_git_repo():
            raise GitRepositoryError(f"Not a git repository: {repo_path}")
    
    def _is_git_repo(self) -> bool:
        """Проверяет, является ли директория Git репозиторием"""
        try:
            self._run_git(['rev-parse', '--git-dir'])
            return True
        except GitCommandError:
            return False
    
    def _run_git(self, args: List[str], input_ Optional[str] = None) -> str:
        """Выполняет Git команду"""
        cmd = ['git'] + args
        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                input=input_data,
                encoding='utf-8'
            )
            if result.returncode != 0:
                raise GitCommandError(cmd, result.returncode, result.stderr)
            return result.stdout.strip()
        except FileNotFoundError:
            raise GitRepositoryError("Git is not installed or not in PATH")
    
    def delete_files_by_name(self, filenames: List[str]) -> Dict[str, int]:
        """
        Удаляет файлы по именам
        
        Args:
            filenames: Список имен файлов для удаления
            
        Returns:
            Словарь с информацией об удаленных файлах
        """
        self.logger.info(f"Deleting files by name: {filenames}")
        return self.cleaner.delete_files_by_name(filenames)
    
    def delete_files_by_pattern(self, patterns: List[str]) -> Dict[str, int]:
        """
        Удаляет файлы по паттернам (glob)
        
        Args:
            patterns: Список паттернов для удаления
            
        Returns:
            Словарь с информацией об удаленных файлах
        """
        self.logger.info(f"Deleting files by pattern: {patterns}")
        return self.cleaner.delete_files_by_pattern(patterns)
    
    def delete_files_larger_than(self, size_str: str) -> Dict[str, int]:
        """
        Удаляет файлы больше указанного размера
        
        Args:
            size_str: Размер в формате '100MB', '1.5GB' и т.д.
            
        Returns:
            Словарь с информацией об удаленных файлах
        """
        size_bytes = parse_size(size_str)
        self.logger.info(f"Deleting files larger than {human_readable_size(size_bytes)}")
        return self.cleaner.delete_files_larger_than(size_bytes)
    
    def replace_text_in_files(self, old_text: str, new_text: str, 
                            file_patterns: Optional[List[str]] = None) -> Dict[str, int]:
        """
        Заменяет текст в файлах
        
        Args:
            old_text: Текст для замены
            new_text: Новый текст
            file_patterns: Паттерны файлов для обработки (None = все файлы)
            
        Returns:
            Словарь с информацией о замененных файлах
        """
        self.logger.info(f"Replacing text in files")
        return self.cleaner.replace_text_in_files(old_text, new_text, file_patterns)
    
    def delete_folders(self, folder_names: List[str]) -> Dict[str, int]:
        """
        Удаляет папки по именам
        
        Args:
            folder_names: Список имен папок для удаления
            
        Returns:
            Словарь с информацией об удаленных папках
        """
        self.logger.info(f"Deleting folders: {folder_names}")
        return self.cleaner.delete_folders(folder_names)
    
    def run_cleanup(self) -> Dict[str, any]:
        """
        Выполняет полную очистку репозитория
        
        Returns:
            Словарь с результатами очистки
        """
        if self.dry_run:
            self.logger.info("DRY RUN MODE - No changes will be made")
        
        # Выполняем очистку
        result = self.cleaner.run_cleanup()
        
        if not self.dry_run:
            # Очищаем мусор
            self._cleanup_git_garbage()
        
        return result
    
    def _cleanup_git_garbage(self):
        """Очищает мусор Git после переписывания истории"""
        self.logger.info("Cleaning up Git garbage...")
        try:
            self._run_git(['reflog', 'expire', '--expire=now', '--all'])
            self._run_git(['gc', '--prune=now'])
        except GitCommandError as e:
            self.logger.warning(f"Failed to cleanup Git garbage: {e}")
    
    def get_stats(self) -> Dict[str, any]:
        """
        Получает статистику репозитория
        
        Returns:
            Словарь со статистикой
        """
        return self.cleaner.get_stats()