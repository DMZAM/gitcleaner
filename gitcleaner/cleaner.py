"""
Основная логика очистки Git репозитория
"""

import os
import subprocess
import logging
from typing import List, Dict, Set, Optional, Callable, Tuple
from pathlib import Path
from tqdm import tqdm

from .exceptions import GitCommandError
from .utils import match_patterns, is_binary_file, human_readable_size

class Cleaner:
    """Класс для выполнения операций очистки"""
    
    def __init__(self, repo_path: str, dry_run: bool = False):
        self.repo_path = Path(repo_path)
        self.dry_run = dry_run
        self.logger = logging.getLogger(__name__)
        
        # Настройки очистки
        self.files_to_delete: Set[str] = set()
        self.patterns_to_delete: List[str] = []
        self.size_threshold: Optional[int] = None
        self.text_replacements: List[Tuple[str, str, Optional[List[str]]]] = []
        self.folders_to_delete: Set[str] = set()
        
        # Статистика
        self.stats = {
            'commits_processed': 0,
            'files_deleted': 0,
            'files_replaced': 0,
            'bytes_removed': 0,
            'commits_rewritten': 0
        }
    
    def delete_files_by_name(self, filenames: List[str]) -> Dict[str, int]:
        """Добавляет файлы для удаления по именам"""
        for filename in filenames:
            self.files_to_delete.add(filename)
        return {'files_added': len(filenames)}
    
    def delete_files_by_pattern(self, patterns: List[str]) -> Dict[str, int]:
        """Добавляет паттерны для удаления файлов"""
        self.patterns_to_delete.extend(patterns)
        return {'patterns_added': len(patterns)}
    
    def delete_files_larger_than(self, size_bytes: int) -> Dict[str, int]:
        """Устанавливает порог размера для удаления файлов"""
        self.size_threshold = size_bytes
        return {'size_threshold': size_bytes}
    
    def replace_text_in_files(self, old_text: str, new_text: str, 
                            file_patterns: Optional[List[str]] = None) -> Dict[str, int]:
        """Добавляет правило замены текста"""
        self.text_replacements.append((old_text, new_text, file_patterns))
        return {'replacements_added': 1}
    
    def delete_folders(self, folder_names: List[str]) -> Dict[str, int]:
        """Добавляет папки для удаления"""
        for folder in folder_names:
            self.folders_to_delete.add(folder)
        return {'folders_added': len(folder_names)}
    
    def run_cleanup(self) -> Dict[str, any]:
        """Выполняет полную очистку"""
        self.logger.info("Starting repository cleanup...")
        
        # Получаем все коммиты
        commits = self._get_all_commits()
        self.logger.info(f"Found {len(commits)} commits to process")
        
        # Карта переписанных коммитов
        commit_map = {}
        
        # Обрабатываем коммиты в обратном порядке (от старых к новым)
        for commit in tqdm(commits, desc="Processing commits", unit="commit"):
            new_commit = self._rewrite_commit(commit)
            commit_map[commit] = new_commit
            self.stats['commits_processed'] += 1
        
        # Обновляем ссылки
        if not self.dry_run:
            self._update_refs(commit_map)
        
        return {
            'stats': self.stats.copy(),
            'commit_map': commit_map if self.dry_run else None
        }
    
    def _get_all_commits(self) -> List[str]:
        """Получает все коммиты в репозитории"""
        try:
            output = self._run_git(['log', '--all', '--pretty=format:%H', '--reverse'])
            return output.splitlines() if output else []
        except GitCommandError:
            return []
    
    def _rewrite_commit(self, commit: str) -> str:
        """Переписывает коммит с учетом правил очистки"""
        try:
            # Получаем дерево коммита
            tree = self._run_git(['rev-parse', f'{commit}^{{tree}}'])
            
            # Получаем все blob'ы в дереве
            blobs = self._get_tree_blobs(tree)
            
            # Формируем новые записи для дерева
            new_entries = []
            files_deleted = 0
            files_replaced = 0
            bytes_removed = 0
            
            for path, blob_info in blobs.items():
                blob_sha, mode = blob_info
                
                # Проверяем, нужно ли удалять файл
                if self._should_delete_file(path, blob_sha):
                    files_deleted += 1
                    self.stats['files_deleted'] += 1
                    continue
                
                # Читаем содержимое файла
                data = self._read_blob(blob_sha)
                original_size = len(data)
                
                # Применяем замены текста
                new_data = self._apply_text_replacements(data, path)
                if new_data != 
                    files_replaced += 1
                    self.stats['files_replaced'] += 1
                
                # Записываем новый blob (если данные изменились)
                if new_data != 
                    if not self.dry_run:
                        new_blob_sha = self._write_blob(new_data)
                    else:
                        new_blob_sha = blob_sha  # В режиме dry-run используем оригинальный SHA
                    bytes_removed += original_size - len(new_data)
                else:
                    new_blob_sha = blob_sha
                
                new_entries.append((mode, 'blob', new_blob_sha, path))
            
            self.stats['bytes_removed'] += bytes_removed
            
            # Обновляем статистику
            if files_deleted > 0 or files_replaced > 0:
                self.stats['commits_rewritten'] += 1
            
            # Создаем новое дерево
            if not self.dry_run:
                new_tree = self._write_tree(new_entries)
            else:
                new_tree = tree  # В режиме dry-run используем оригинальное дерево
            
            # Создаем новый коммит
            if not self.dry_run:
                parent = self._get_commit_parent(commit)
                message = self._get_commit_message(commit)
                new_commit = self._write_commit(parent, new_tree, message)
            else:
                new_commit = commit  # В режиме dry-run используем оригинальный коммит
            
            return new_commit
            
        except Exception as e:
            self.logger.warning(f"Failed to rewrite commit {commit}: {e}")
            return commit  # Возвращаем оригинальный коммит в случае ошибки
    
    def _should_delete_file(self, path: str, blob_sha: str) -> bool:
        """Проверяет, нужно ли удалить файл"""
        
        # Удаление по имени файла
        filename = os.path.basename(path)
        if filename in self.files_to_delete:
            return True
        
        # Удаление по паттернам
        if self.patterns_to_delete and match_patterns(path, self.patterns_to_delete):
            return True
        
        # Удаление по размеру
        if self.size_threshold is not None:
            try:
                size_output = self._run_git(['cat-file', '-s', blob_sha])
                size = int(size_output)
                if size > self.size_threshold:
                    return True
            except (GitCommandError, ValueError):
                pass
        
        # Удаление по имени папки
        path_parts = Path(path).parts
        for folder in self.folders_to_delete:
            if folder in path_parts:
                return True
        
        return False
    
    def _apply_text_replacements(self,  bytes, path: str) -> bytes:
        """Применяет замены текста к данным"""
        if not self.text_replacements:
            return data
        
        # Пропускаем бинарные файлы
        if is_binary_file(data):
            return data
        
        try:
            text_data = data.decode('utf-8')
            modified = False
            
            for old_text, new_text, file_patterns in self.text_replacements:
                # Проверяем паттерны файлов, если указаны
                if file_patterns and not match_patterns(path, file_patterns):
                    continue
                
                if old_text in text_
                    text_data = text_data.replace(old_text, new_text)
                    modified = True
            
            if modified:
                return text_data.encode('utf-8')
            else:
                return data
                
        except UnicodeDecodeError:
            # Не смогли декодировать как UTF-8 - пропускаем
            return data
    
    def _get_tree_blobs(self, tree: str) -> Dict[str, Tuple[str, str]]:
        """Получает все blob'ы в дереве"""
        try:
            output = self._run_git(['ls-tree', '-r', tree])
            blobs = {}
            for line in output.splitlines():
                if line:
                    parts = line.split(None, 3)
                    if len(parts) >= 4:
                        mode, type_, sha, path = parts[0], parts[1], parts[2], parts[3]
                        blobs[path] = (sha, mode)
            return blobs
        except GitCommandError:
            return {}
    
    def _read_blob(self, sha: str) -> bytes:
        """Читает содержимое blob'а"""
        try:
            result = subprocess.run(
                ['git', 'cat-file', 'blob', sha],
                cwd=self.repo_path,
                capture_output=True
            )
            if result.returncode == 0:
                return result.stdout
            else:
                raise GitCommandError(['git', 'cat-file', 'blob', sha], result.returncode, result.stderr.decode())
        except FileNotFoundError:
            raise GitCommandError(['git', 'cat-file', 'blob', sha], 1, "Git not found")
    
    def _write_blob(self,  bytes) -> str:
        """Записывает blob и возвращает его SHA"""
        result = subprocess.run(
            ['git', 'hash-object', '-w', '--stdin'],
            cwd=self.repo_path,
            input=data,
            capture_output=True
        )
        if result.returncode == 0:
            return result.stdout.decode().strip()
        else:
            raise GitCommandError(['git', 'hash-object', '-w', '--stdin'], result.returncode, result.stderr.decode())
    
    def _write_tree(self, entries: List[Tuple[str, str, str, str]]) -> str:
        """Создает новое дерево из записей"""
        if not entries:
            # Создаем пустое дерево
            result = subprocess.run(
                ['git', 'mktree'],
                cwd=self.repo_path,
                input='',
                capture_output=True,
                text=True
            )
        else:
            mktree_input = '\n'.join([f'{mode} {type} {sha}\t{path}' for mode, type, sha, path in entries]) + '\n'
            result = subprocess.run(
                ['git', 'mktree'],
                cwd=self.repo_path,
                input=mktree_input,
                capture_output=True,
                text=True
            )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            raise GitCommandError(['git', 'mktree'], result.returncode, result.stderr)
    
    def _write_commit(self, parent: Optional[str], tree: str, message: str) -> str:
        """Создает новый коммит"""
        cmd = ['commit-tree', tree]
        if parent:
            cmd.extend(['-p', parent])
        cmd.extend(['-m', message])
        
        result = subprocess.run(
            ['git'] + cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            raise GitCommandError(['git'] + cmd, result.returncode, result.stderr)
    
    def _get_commit_parent(self, commit: str) -> Optional[str]:
        """Получает родительский коммит"""
        try:
            output = self._run_git(['rev-parse', f'{commit}^'])
            return output if output else None
        except GitCommandError:
            return None
    
    def _get_commit_message(self, commit: str) -> str:
        """Получает сообщение коммита"""
        try:
            return self._run_git(['log', '--format=%B', '-n', '1', commit])
        except GitCommandError:
            return "No message"
    
    def _update_refs(self, commit_map: Dict[str, str]):
        """Обновляет ссылки на новые коммиты"""
        try:
            # Получаем все ссылки
            refs_output = self._run_git(['show-ref', '--heads'])
            refs = []
            for line in refs_output.splitlines():
                if line:
                    sha, ref = line.split(None, 1)
                    refs.append((sha, ref))
            
            # Обновляем ссылки
            for old_sha, ref_name in refs:
                if old_sha in commit_map:
                    new_sha = commit_map[old_sha]
                    if new_sha != old_sha:
                        self._run_git(['update-ref', ref_name, new_sha])
                        self.logger.info(f"Updated {ref_name} from {old_sha[:8]} to {new_sha[:8]}")
        
        except GitCommandError as e:
            self.logger.warning(f"Failed to update refs: {e}")
    
    def _run_git(self, args: List[str]) -> str:
        """Выполняет Git команду"""
        cmd = ['git'] + args
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise GitCommandError(cmd, result.returncode, result.stderr)
        return result.stdout.strip()
    
    def get_stats(self) -> Dict[str, any]:
        """Получает текущую статистику"""
        return self.stats.copy()