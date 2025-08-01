"""
Исключения для GitCleaner
"""

class GitCleanerError(Exception):
    """Базовое исключение для GitCleaner"""
    pass

class GitRepositoryError(GitCleanerError):
    """Ошибка работы с Git репозиторием"""
    pass

class InvalidPathError(GitCleanerError):
    """Неверный путь к файлу или директории"""
    pass

class InvalidSizeError(GitCleanerError):
    """Неверный размер файла"""
    pass

class GitCommandError(GitCleanerError):
    """Ошибка выполнения Git команды"""
    def __init__(self, command, returncode, stderr):
        self.command = command
        self.returncode = returncode
        self.stderr = stderr
        super().__init__(f"Git command failed: {' '.join(command)} (exit code {returncode}): {stderr}")