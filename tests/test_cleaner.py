"""
Тесты для GitCleaner
"""

import os
import tempfile
import subprocess
import pytest
from pathlib import Path

from gitcleaner.core import GitCleaner
from gitcleaner.exceptions import GitRepositoryError

class TestGitCleaner:
    """Тесты для GitCleaner"""
    
    def setup_method(self):
        """Создает временный Git репозиторий для тестов"""
        self.temp_dir = tempfile.mkdtemp()
        self.repo_path = Path(self.temp_dir)
        
        # Инициализируем Git репозиторий
        subprocess.run(['git', 'init'], cwd=self.repo_path, capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=self.repo_path, capture_output=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=self.repo_path, capture_output=True)
        
        # Создаем тестовые файлы
        (self.repo_path / 'test.txt').write_text('Hello World')
        (self.repo_path / 'secret.key').write_text('SECRET_KEY=12345')
        (self.repo_path / 'large_file.bin').write_bytes(b'0' * 1024 * 1024)  # 1MB файл
        
        # Делаем коммит
        subprocess.run(['git', 'add', '.'], cwd=self.repo_path, capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=self.repo_path, capture_output=True)
    
    def teardown_method(self):
        """Удаляет временный репозиторий"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_init_with_valid_repo(self):
        """Тест инициализации с валидным репозиторием"""
        cleaner = GitCleaner(str(self.repo_path))
        assert cleaner.repo_path == self.repo_path
    
    def test_init_with_invalid_repo(self):
        """Тест инициализации с невалидным репозиторием"""
        with pytest.raises(GitRepositoryError):
            GitCleaner('/non/existent/path')
    
    def test_delete_files_by_name(self):
        """Тест удаления файлов по имени"""
        cleaner = GitCleaner(str(self.repo_path), dry_run=True)
        result = cleaner.delete_files_by_name(['secret.key'])
        assert result['files_added'] == 1
    
    def test_delete_files_by_pattern(self):
        """Тест удаления файлов по паттерну"""
        cleaner = GitCleaner(str(self.repo_path), dry_run=True)
        result = cleaner.delete_files_by_pattern(['*.key'])
        assert result['patterns_added'] == 1
    
    def test_delete_files_larger_than(self):
        """Тест удаления файлов по размеру"""
        cleaner = GitCleaner(str(self.repo_path), dry_run=True)
        result = cleaner.delete_files_larger_than('500KB')
        assert result['size_threshold'] == 512000  # 500KB в байтах
    
    def test_replace_text_in_files(self):
        """Тест замены текста в файлах"""
        cleaner = GitCleaner(str(self.repo_path), dry_run=True)
        result = cleaner.replace_text_in_files('Hello', 'Hi')
        assert result['replacements_added'] == 1
    
    def test_delete_folders(self):
        """Тест удаления папок"""
        # Создаем папку
        folder_path = self.repo_path / 'sensitive'
        folder_path.mkdir()
        (folder_path / 'passwords.txt').write_text('password123')
        
        # Добавляем в Git
        subprocess.run(['git', 'add', '.'], cwd=self.repo_path, capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'Add sensitive folder'], cwd=self.repo_path, capture_output=True)
        
        cleaner = GitCleaner(str(self.repo_path), dry_run=True)
        result = cleaner.delete_folders(['sensitive'])
        assert result['folders_added'] == 1

if __name__ == '__main__':
    pytest.main([__file__])