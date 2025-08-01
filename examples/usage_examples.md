# 📚 Примеры использования GitCleaner

## 🎯 Основные сценарии

### 1. Удаление секретов

```bash
# Удалить файлы с секретами
gitcleaner clean --file .env --file config.json --file secrets.yaml

# Удалить файлы по паттернам
gitcleaner clean --pattern "*.key" --pattern "*.pem" --pattern "id_rsa*"
```

### 2. Очистка логов и временных файлов

```bash
# Удалить все логи и временные файлы
gitcleaner clean --pattern "*.log" --pattern "*.tmp" --pattern "temp/*"
```

### 3. Удаление больших файлов

```bash
# Удалить файлы больше 100MB
gitcleaner clean --size 100MB

# Удалить очень большие файлы (>1GB)
gitcleaner clean --size 1GB
```

### 4. Замена чувствительной информации

```bash
# Заменить пароли в файлах конфигурации
gitcleaner clean \
  --replace-old "password=.*" \
  --replace-new "password=REDACTED" \
  --replace-files "*.conf,*.yaml,*.yml"

# Заменить API ключи
gitcleaner clean \
  --replace-old "API_KEY=[A-Za-z0-9]+" \
  --replace-new "API_KEY=REDACTED"
```

## 🏢 Корпоративные сценарии

### Очистка репозитория перед открытием OSS

```bash
# Комплексная очистка перед публикацией
gitcleaner clean \
  --file .env \
  --file credentials.json \
  --file "*.key" \
  --pattern "internal/*" \
  --pattern "*.log" \
  --size 50MB \
  --replace-old "COMPANY_API_KEY=.*" \
  --replace-new "COMPANY_API_KEY=REDACTED"
```

### Очистка после миграции

```bash
# Удалить старые артефакты после миграции
gitcleaner clean \
  --folder legacy \
  --folder old_version \
  --pattern "*.old" \
  --pattern "migration_backup/*"
```

## 🛡️ Безопасность

### Пошаговая очистка

```bash
# 1. Проверить репозиторий
gitcleaner verify

# 2. Посмотреть статистику
gitcleaner stats

# 3. Выполнить dry-run
gitcleaner clean --dry-run --file secret.txt

# 4. Применить изменения
gitcleaner clean --file secret.txt

# 5. Очистить мусор
git reflog expire --expire=now --all
git gc --prune=now

# 6. Запушить изменения
git push --force-with-lease origin main
```

## 📊 Мониторинг

### Проверка результатов

```bash
# Посмотреть статистику после очистки
gitcleaner stats

# Проверить размер репозитория
du -sh .git

# Проверить историю
git log --oneline
```

## ⚙️ Продвинутые примеры

### Скрипт для регулярной очистки

```bash
#!/bin/bash
# cleanup.sh

echo "Начинаем очистку репозитория..."

# Удалить временные файлы
gitcleaner clean --pattern "*.tmp" --pattern "*.log" --pattern "temp/*"

# Удалить большие файлы (>100MB)
gitcleaner clean --size 100MB

# Очистить мусор Git
git reflog expire --expire=now --all
git gc --prune=now

echo "Очистка завершена!"
```

### Интеграция с CI/CD

```yaml
# .github/workflows/cleanup.yml
name: Repository Cleanup

on:
  schedule:
    - cron: '0 2 * * 0'  # Каждое воскресенье в 2:00

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Install GitCleaner
        run: pip install gitcleaner
      
      - name: Clean repository
        run: |
          gitcleaner clean --pattern "*.log" --size 50MB --dry-run
          # gitcleaner clean --pattern "*.log" --size 50MB  # Раскомментируйте для применения
      
      - name: Cleanup Git garbage
        run: |
          git reflog expire --expire=now --all
          git gc --prune=now
      
      - name: Push changes
        run: |
          git push --force-with-lease origin main
        if: false  # Установите в true для применения изменений
```

## 🎨 Примеры с различными опциями

### Подробный вывод

```bash
# Запуск с подробным логированием
gitcleaner clean --verbose --dry-run --file secret.txt
```

### Работа с конкретными ветками

```bash
# Очистить только определенные ветки
gitcleaner clean --pattern "*.log" --dry-run

# Затем обновить только нужные ветки
git push --force-with-lease origin main develop
```

### Массовая очистка

```bash
# Очистка множества файлов
gitcleaner clean \
  --file .env \
  --file .env.local \
  --file .env.production \
  --file config/secrets.json \
  --file keys/private.key \
  --pattern "*.log" \
  --pattern "logs/*" \
  --pattern "tmp/*" \
  --pattern "*.tmp" \
  --pattern "*.cache" \
  --size 100MB
```

## 🧪 Тестирование перед применением

### Dry-run режим

```bash
# Всегда начинайте с dry-run
gitcleaner clean --dry-run --file secret.txt

# Проверьте статистику
gitcleaner stats
```

### Проверка изменений

```bash
# Проверить, что файлы будут удалены
gitcleaner clean --dry-run --pattern "*.log" | grep "files_deleted"

# Проверить размер до и после
echo "Before:" && du -sh .git
gitcleaner clean --dry-run --size 100MB
echo "After (estimated):" && gitcleaner stats
```

## 🚀 Производительность

### Для больших репозиториев

```bash
# Используйте verbose для отслеживания прогресса
gitcleaner clean --verbose --pattern "*.log" --size 50MB

# Очистка по частям
gitcleaner clean --pattern "*.log" --dry-run
gitcleaner clean --pattern "temp/*" --dry-run
gitcleaner clean --size 100MB --dry-run
```

### Параллельная обработка

```bash
# GitCleaner автоматически обрабатывает коммиты с прогресс-баром
gitcleaner clean --pattern "*.tmp" --verbose
```

## 🛠️ Устранение неполадок

### Частые проблемы

```bash
# Если получаете ошибки доступа
git clean -fd  # Очистить неотслеживаемые файлы
git reset --hard HEAD  # Сбросить рабочую директорию

# Если нужно отменить изменения
git reflog  # Посмотреть историю
git reset --hard HEAD@{1}  # Откатиться на один шаг
```

### Логирование

```bash
# Подробное логирование
gitcleaner clean --verbose --dry-run --file secret.txt 2>&1 | tee cleanup.log
```

## 📋 Рекомендации

1. **Всегда делайте резервную копию перед очисткой**
2. **Используйте `--dry-run` для тестирования**
3. **Проверяйте статистику до и после**
4. **Используйте `--force-with-lease` вместо `--force`**
5. **Уведомите команду перед пушем изменений**
6. **Проверяйте .gitignore после очистки**

## 🎯 Лучшие практики

### Регулярное обслуживание

```bash
# Еженедельная очистка
0 2 * * 0 cd /path/to/repo && gitcleaner clean --pattern "*.log" --size 50MB
```

### Предварительная проверка

```bash
# Проверить большие файлы перед очисткой
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | sed -n 's/^blob //p' | sort --numeric-sort --key=2 | cut -c 1-12,41- | $(command -v gnumsort || echo sort) --numeric-sort --key=2
```

### Комплексная очистка

```bash
# Полная очистка репозитория
gitcleaner clean \
  --pattern "*.log" \
  --pattern "*.tmp" \
  --pattern "temp/*" \
  --pattern "*.cache" \
  --size 100MB \
  --folder node_modules \
  --folder .pytest_cache \
  --file .env

# Очистить мусор Git
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```
