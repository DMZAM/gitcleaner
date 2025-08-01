"""
CLI интерфейс для GitCleaner
"""

import os
import sys
import logging
from pathlib import Path
import click
from colorama import init, Fore, Style

from .core import GitCleaner
from .exceptions import GitCleanerError
from .utils import human_readable_size, parse_size

# Инициализация colorama
init(autoreset=True)

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@click.group()
@click.version_option()
def main():
    """GitCleaner - Аналог BFG Repo-Cleaner на Python"""
    pass

@main.command()
@click.option('-p', '--path', default='.', help='Путь к Git репозиторию')
@click.option('--dry-run', is_flag=True, help='Режим пробного запуска (без изменений)')
@click.option('-v', '--verbose', is_flag=True, help='Подробный вывод')
def stats(path, dry_run, verbose):
    """Показать статистику репозитория"""
    try:
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        cleaner = GitCleaner(path, dry_run)
        stats = cleaner.get_stats()
        
        click.echo(f"{Fore.CYAN}Статистика репозитория:{Style.RESET_ALL}")
        click.echo(f"  Путь: {path}")
        click.echo(f"  Режим dry-run: {'Да' if dry_run else 'Нет'}")
        click.echo()
        click.echo(f"{Fore.GREEN}Статистика:{Style.RESET_ALL}")
        for key, value in stats.items():
            click.echo(f"  {key}: {value}")
            
    except GitCleanerError as e:
        click.echo(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)

@main.command()
@click.option('-p', '--path', default='.', help='Путь к Git репозиторию')
@click.option('--dry-run', is_flag=True, help='Режим пробного запуска (без изменений)')
@click.option('-f', '--file', multiple=True, help='Имена файлов для удаления')
@click.option('--pattern', multiple=True, help='Паттерны файлов для удаления (glob)')
@click.option('--size', help='Удалить файлы больше указанного размера (например: 100MB, 1.5GB)')
@click.option('--folder', multiple=True, help='Имена папок для удаления')
@click.option('--replace-old', help='Текст для замены')
@click.option('--replace-new', help='Новый текст')
@click.option('--replace-files', help='Паттерны файлов для замены текста')
@click.option('-v', '--verbose', is_flag=True, help='Подробный вывод')
def clean(path, dry_run, file, pattern, size, folder, replace_old, replace_new, replace_files, verbose):
    """Очистить репозиторий"""
    try:
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        cleaner = GitCleaner(path, dry_run)
        
        # Добавляем файлы для удаления
        if file:
            result = cleaner.delete_files_by_name(list(file))
            click.echo(f"{Fore.GREEN}Добавлено файлов для удаления: {result['files_added']}{Style.RESET_ALL}")
        
        # Добавляем паттерны для удаления
        if pattern:
            result = cleaner.delete_files_by_pattern(list(pattern))
            click.echo(f"{Fore.GREEN}Добавлено паттернов для удаления: {result['patterns_added']}{Style.RESET_ALL}")
        
        # Удаление по размеру
        if size:
            result = cleaner.delete_files_larger_than(size)
            size_bytes = result['size_threshold']
            click.echo(f"{Fore.GREEN}Установлен порог размера: {human_readable_size(size_bytes)}{Style.RESET_ALL}")
        
        # Удаление папок
        if folder:
            result = cleaner.delete_folders(list(folder))
            click.echo(f"{Fore.GREEN}Добавлено папок для удаления: {result['folders_added']}{Style.RESET_ALL}")
        
        # Замена текста
        if replace_old and replace_new:
            file_patterns = replace_files.split(',') if replace_files else None
            result = cleaner.replace_text_in_files(replace_old, replace_new, file_patterns)
            click.echo(f"{Fore.GREEN}Добавлено правил замены текста: {result['replacements_added']}{Style.RESET_ALL}")
        
        # Выполняем очистку
        click.echo(f"\n{Fore.YELLOW}Начинаем очистку...{Style.RESET_ALL}")
        result = cleaner.run_cleanup()
        
        # Показываем результаты
        stats = result['stats']
        click.echo(f"\n{Fore.CYAN}Результаты очистки:{Style.RESET_ALL}")
        click.echo(f"  Обработано коммитов: {stats['commits_processed']}")
        click.echo(f"  Удалено файлов: {stats['files_deleted']}")
        click.echo(f"  Заменено файлов: {stats['files_replaced']}")
        click.echo(f"  Удалено данных: {human_readable_size(stats['bytes_removed'])}")
        click.echo(f"  Переписано коммитов: {stats['commits_rewritten']}")
        
        if dry_run:
            click.echo(f"\n{Fore.YELLOW}Это был пробный запуск. Никаких изменений не было сделано.{Style.RESET_ALL}")
            click.echo(f"{Fore.YELLOW}Для применения изменений запустите команду без флага --dry-run{Style.RESET_ALL}")
        else:
            click.echo(f"\n{Fore.GREEN}Очистка завершена успешно!{Style.RESET_ALL}")
            click.echo(f"{Fore.YELLOW}Не забудьте запустить: git push --force-with-lease{Style.RESET_ALL}")
            
    except GitCleanerError as e:
        click.echo(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"{Fore.RED}Неожиданная ошибка: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)

@main.command()
@click.option('-p', '--path', default='.', help='Путь к Git репозиторию')
def verify(path):
    """Проверить, что репозиторий готов для очистки"""
    try:
        cleaner = GitCleaner(path)
        click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} Репозиторий найден: {path}")
        click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} Git доступен")
        
        # Проверяем наличие коммитов
        commits = cleaner.cleaner._get_all_commits()
        click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} Найдено коммитов: {len(commits)}")
        
        # Проверяем текущую ветку
        try:
            branch = cleaner.cleaner._run_git(['rev-parse', '--abbrev-ref', 'HEAD'])
            click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} Текущая ветка: {branch}")
        except:
            pass
            
        click.echo(f"\n{Fore.GREEN}Репозиторий готов для очистки!{Style.RESET_ALL}")
        
    except GitCleanerError as e:
        click.echo(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    main()