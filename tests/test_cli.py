"""
Тесты для CLI интерфейса
"""

import os
import tempfile
import subprocess
import pytest
from click.testing import CliRunner
from pathlib import Path

from gitcleaner.cli import main

class TestCLI:
    """Тесты для CLI интерфейса"""
    
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
        
        # Делаем коммит
        subprocess.run(['git', 'add', '.'], cwd=self.repo_path, capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=self.repo_path, capture_output=True)
    
    def teardown_method(self):
        """Удаляет временный репозиторий"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_version(self):
        """Тест команды версии"""
        runner = CliRunner()
        result = runner.invoke(main, ['--version'])
        assert result.exit_code == 0
        assert 'GitCleaner' in result.output
    
    def test_stats_command(self):
        """Тест команды статистики"""
        runner = CliRunner()
        result = runner.invoke(main, ['stats', '--path', str(self.repo_path)])
        assert result.exit_code == 0
        assert 'Статистика репозитория' in result.output
    
    def test_verify_command(self):
        """Тест команды проверки"""
        runner = CliRunner()
        result = runner.invoke(main, ['verify', '--path', str(self.repo_path)])
        assert result.exit_code == 0
        assert 'Репозиторий готов для очистки' in result.output
    
    def test_clean_command_dry_run(self):
        """Тест команды очистки в режиме dry-run"""
        runner = CliRunner()
        result = runner.invoke(main, [
            'clean',
            '--path', str(self.repo_path),
            '--dry-run',
            '--file', 'secret.key',
            '--pattern', '*.txt'
        ])
        assert result.exit_code == 0
        assert 'Это был пробный запуск' in result.output

if __name__ == '__main__':
    pytest.main([__file__])