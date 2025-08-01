
# 🧹 GitCleaner

[![PyPI version](https://badge.fury.io/py/gitcleaner.svg)](https://badge.fury.io/py/gitcleaner)
[![Python Version](https://img.shields.io/pypi/pyversions/gitcleaner.svg)](https://pypi.org/project/gitcleaner/)
[![License](https://img.shields.io/pypi/l/gitcleaner.svg)](https://github.com/DMZAM/gitcleaner/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/gitcleaner)](https://pepy.tech/project/gitcleaner)

Аналог [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) на Python для очистки Git репозиториев от больших файлов, секретов и другой чувствительной информации.

## 🌟 Особенности

- ✅ **Удаление файлов по именам** - Удаляйте конкретные файлы по их именам
- ✅ **Удаление файлов по паттернам** - Используйте glob-паттерны для массового удаления
- ✅ **Удаление больших файлов** - Автоматически удаляйте файлы больше заданного размера
- ✅ **Замена текста** - Безопасно заменяйте чувствительную информацию в файлах
- ✅ **Удаление папок** - Полностью удаляйте нежелательные директории
- ✅ **Режим dry-run** - Тестируйте операции без реальных изменений
- ✅ **Прогресс-бар** - Визуализация процесса очистки для больших репозиториев
- ✅ **Подробная статистика** - Получайте детальную информацию о проделанной работе
- ✅ **Кроссплатформенность** - Работает на Windows, macOS и Linux
- ✅ **CLI интерфейс** - Удобное командное управление

## 📦 Установка

### Из PyPI (рекомендуется)

```bash
pip install gitcleaner
```

### Из исходников

```bash
git clone https://github.com/DMZAM/gitcleaner.git
cd gitcleaner
pip install -r requirements.txt
pip install -e .
```

### Установка для разработки

```bash
pip install -e ".[dev]"
```

## 🚀 Быстрый старт

### Проверка репозитория

```bash
# Проверить, что репозиторий готов для очистки
gitcleaner verify

# Посмотреть текущую статистику
gitcleaner stats
```

### Основные сценарии использования

#### Удаление секретов

```bash
# Удалить файлы с секретами в режиме просмотра
gitcleaner clean --dry-run --file .env --file config.json

# Применить изменения
gitcleaner clean --file .env --file config.json
```

#### Удаление логов и временных файлов

```bash
# Удалить все логи и временные файлы
gitcleaner clean --pattern "*.log" --pattern "*.tmp" --pattern "temp/*"
```

#### Удаление больших файлов

```bash
# Удалить файлы больше 100MB
gitcleaner clean --size 100MB

# Удалить очень большие файлы (>1GB)
gitcleaner clean --size 1GB
```

#### Замена чувствительной информации

```bash
# Заменить пароли в файлах конфигурации
gitcleaner clean \
  --replace-old "password=.*" \
  --replace-new "password=REDACTED" \
  --replace-files "*.conf,*.yaml,*.yml"
```

## 📚 Подробное использование

### Все опции команды clean

```bash
gitcleaner clean [OPTIONS]
```

**Опции:**
- `-p, --path PATH` - Путь к Git репозиторию (по умолчанию: текущая директория)
- `--dry-run` - Режим пробного запуска (без изменений)
- `-f, --file FILE` - Имена файлов для удаления (можно указывать несколько раз)
- `--pattern PATTERN` - Паттерны файлов для удаления (glob) (можно указывать несколько раз)
- `--size SIZE` - Удалить файлы больше указанного размера (например: 100MB, 1.5GB)
- `--folder FOLDER` - Имена папок для удаления (можно указывать несколько раз)
- `--replace-old TEXT` - Текст для замены
- `--replace-new TEXT` - Новый текст
- `--replace-files TEXT` - Паттерны файлов для замены текста (через запятую)
- `-v, --verbose` - Подробный вывод
- `--help` - Показать справку

### Примеры комплексной очистки

```bash
# Комбинированная очистка
gitcleaner clean \
  --file .env \
  --file secrets.json \
  --pattern "*.log" \
  --pattern "temp/*" \
  --size 50MB \
  --folder node_modules \
  --replace-old "API_KEY=.*" \
  --replace-new "API_KEY=REDACTED" \
  --replace-files "*.conf,*.yaml"
```

### Работа с конкретным репозиторием

```bash
gitcleaner clean --path /path/to/repo --file secret.txt
```

## ⚙️ После очистки

После выполнения очистки обязательно выполните следующие команды:

```bash
# Очистить мусор Git
git reflog expire --expire=now --all
git gc --prune=now

# Запушить изменения (ОСТОРОЖНО!)
git push --force-with-lease origin main
```

## 🛠️ Разработка

### Запуск тестов

```bash
# Установка зависимостей для разработки
pip install -e ".[dev]"

# Запуск тестов
pytest tests/

# Запуск тестов с покрытием
pytest tests/ --cov=gitcleaner --cov-report=html
```

### Форматирование кода

```bash
# Форматирование с помощью black
black gitcleaner/ tests/

# Проверка с помощью flake8
flake8 gitcleaner/ tests/
```

### Запуск с подробным выводом

```bash
gitcleaner clean --verbose --dry-run --file secret.txt
```

## 📊 Команды CLI

### verify - Проверка репозитория

```bash
gitcleaner verify [--path PATH]
```

Проверяет, что указанная директория является Git репозиторием и готова к очистке.

### stats - Статистика репозитория

```bash
gitcleaner stats [--path PATH] [--dry-run] [--verbose]
```

Показывает статистику репозитория и текущие настройки очистки.

### clean - Очистка репозитория

```bash
gitcleaner clean [OPTIONS]
```

Основная команда для очистки репозитория.

## 📁 Структура проекта

```
gitcleaner/
├── gitcleaner/           # Основной код
│   ├── __init__.py      # Инициализация пакета
│   ├── core.py         # Основной класс GitCleaner
│   ├── cleaner.py      # Логика очистки
│   ├── cli.py          # CLI интерфейс
│   ├── utils.py        # Вспомогательные функции
│   └── exceptions.py   # Исключения
├── tests/              # Тесты
│   ├── __init__.py
│   ├── test_cleaner.py
│   └── test_cli.py
├── examples/           # Примеры использования
│   └── usage_examples.md
├── README.md           # Документация
├── setup.py            # Конфигурация установки
├── requirements.txt    # Зависимости
└── LICENSE             # Лицензия
```

## ⚠️ Предупреждения

### ⚠️ ВАЖНО: Безопасность

- **Всегда делайте резервную копию репозитория перед очисткой**
- **Очистка переписывает историю Git - используйте `--force-with-lease` при пуше**
- **Не используйте на публичных репозиториях без согласия команды**
- **Тщательно тестируйте в режиме `--dry-run` перед применением изменений**

### 🚨 Последствия очистки

1. **История коммитов будет переписана**
2. **SHA хэши коммитов изменятся**
3. **Необходимо использовать `git push --force-with-lease` для пуша**
4. **Другие разработчики должны выполнить `git fetch` и `git reset`**

## 🆘 Устранение неполадок

### Частые проблемы

**Ошибка: "Not a git repository"**
```bash
# Убедитесь, что вы находитесь в директории репозитория
cd /path/to/your/repo
git status  # Проверьте, что это Git репозиторий
```

**Ошибка: "Git is not installed"**
```bash
# Убедитесь, что Git установлен
git --version
```

**Отмена изменений**
```bash
# Если что-то пошло не так, можно отменить изменения
git reflog  # Посмотреть историю
git reset --hard HEAD@{1}  # Откатиться на один шаг назад
```

## 📈 Примеры статистики

После очистки вы получите подробную статистику:

```
Результаты очистки:
  Обработано коммитов: 150
  Удалено файлов: 25
  Заменено файлов: 8
  Удалено данных: 256.3MB
  Переписано коммитов: 42
```

## 🤝 Вклад в проект

Приветствуются pull request'ы и issue reports!

### Как внести вклад

1. Форкните репозиторий
2. Создайте ветку для вашей функции (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Запушьте ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

### Разработка

```bash
# Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установите пакет в режиме разработки
pip install -e ".[dev]"

# Запустите тесты
pytest tests/
```

## 📄 Лицензия

Распространяется под лицензией MIT. Смотрите файл [LICENSE](LICENSE) для подробной информации.

## 🙏 Благодарности

- Вдохновлен [BFG Repo-Cleaner](https://github.com/rtyley/bfg-repo-cleaner) от Roberto Tyley
- Использует отличные библиотеки: [Click](https://github.com/pallets/click), [tqdm](https://github.com/tqdm/tqdm), [colorama](https://github.com/tartley/colorama)

## 📞 Поддержка

Если у вас есть вопросы или проблемы:

1. Проверьте [Issues](https://github.com/DMZAM/gitcleaner/issues)
2. Создайте новый issue с подробным описанием проблемы
3. Укажите версию Python, Git и операционной системы

## 🔄 Сравнение с BFG Repo-Cleaner

| Функция | GitCleaner | BFG Repo-Cleaner |
|---------|------------|------------------|
| Удаление файлов по имени | ✅ | ✅ |
| Удаление по паттернам | ✅ | ✅ |
| Удаление больших файлов | ✅ | ✅ |
| Замена текста | ✅ | ✅ |
| Удаление папок | ✅ | ⚠️ (ограниченно) |
| Python реализация | ✅ | ❌ (Scala) |
| CLI интерфейс | ✅ | ✅ |
| Прогресс-бар | ✅ | ❌ |
| Подробная статистика | ✅ | ⚠️ |

## 📚 Дополнительные ресурсы

- [Примеры использования](examples/usage_examples.md)
- [Документация API](https://github.com/DMZAM/gitcleaner/wiki)
- [Часто задаваемые вопросы](https://github.com/DMZAM/gitcleaner/wiki/FAQ)
