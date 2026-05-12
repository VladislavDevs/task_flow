# Тестирование Task Flow Backend

Данный документ описывает процесс запуска тестов для проекта Task Flow.  
Тесты используют тестовую базу данных PostgreSQL, разворачиваемую в Docker-контейнере.

---

## 1. Предварительные требования

- **Python 3.12+** (рекомендуется версия, указанная в `runtime.txt` или `pyproject.toml`)
- **Docker Desktop** (или Docker Engine + Docker Compose) – для запуска тестовой PostgreSQL
- Виртуальное окружение с установленными зависимостями

---

## 2. Подготовка окружения

Откройте терминал в корне проекта и перейдите в директорию `backend`:

```bash
cd backend
```

Активируйте виртуальное окружение:

- **Windows**:
  ```bash
  .venv\Scripts\activate
  ```
- **Linux / macOS**:
  ```bash
  source .venv/bin/activate
  ```

Установите зависимости, необходимые для тестирования:

```bash
pip install -r requirements.txt
pip install pytest pytest-cov
```

> **Примечание**: `pytest-cov` необходим для формирования отчёта о покрытии кода.

---

## 3. Запуск тестовой базы данных

Используйте подготовленный файл `docker-compose.test.yml`, который поднимает PostgreSQL на порту **5433** (чтобы не конфликтовать с основной базой данных).

Запустите контейнер:

```bash
docker-compose -f docker-compose.test.yml up -d
```

Подождите несколько секунд, пока база данных станет доступна. Убедиться в успешном запуске можно командой:

```bash
docker ps
```

Вы должны увидеть контейнер с именем `backend-test_db-1` (или подобным), использующий образ `postgres:15`.

Параметры подключения к тестовой БД:

| Параметр    | Значение      |
|-------------|---------------|
| Хост        | localhost     |
| Порт        | 5433          |
| Пользователь| test_user     |
| Пароль      | test_pass     |
| База данных | test_db       |

URL подключения:  
`postgresql://test_user:test_pass@localhost:5433/test_db`

Именно этот URL жёстко прописан в `tests/conftest.py`. Если по какой-то причине порт или учётные данные нужно изменить, отредактируйте оба файла: `docker-compose.test.yml` и `tests/conftest.py`.

---

## 4. Запуск тестов

Находясь в директории `backend`, выполните:

```bash
pytest -v
```

Для получения отчёта о покрытии кода:

```bash
pytest -v --cov=app --cov-report=term-missing
```

### 4.1. Фильтрация тестов

- **Запуск конкретного файла**:
  ```bash
  pytest tests/test_models.py -v
  ```
- **Запуск одного тестового класса**:
  ```bash
  pytest tests/test_models.py::TestUser -v
  ```
- **Запуск отдельного теста**:
  ```bash
  pytest tests/test_models.py::TestUser::test_create_and_retrieve -v
  ```

---

## 5. Остановка тестовой БД

После завершения тестирования остановите и удалите контейнер:

```bash
docker-compose -f docker-compose.test.yml down
```

Если необходимо полностью удалить том с данными (чтобы при следующем запуске база создалась заново):

```bash
docker-compose -f docker-compose.test.yml down -v
```

---

## 6. Структура тестов

```
backend/tests/
├── conftest.py                 # Общие фикстуры (подключение к БД, клиент)
├── test_models.py              # Тесты для SQLAlchemy-моделей (User, Task, Category)
├── test_core/
│   └── test_database.py        # Тесты для модуля core/database.py
├── test_api/
│   ├── test_auth.py            # Тесты эндпоинтов авторизации (/auth/*)
│   └── test_tasks.py           # Тесты эндпоинтов задач (/tasks/*)
└── test_services/              # (опционально) тесты бизнес-логики
```

---

## 7. Возможные проблемы и их решение

### Ошибка «faield to connect to database» или «Connection refused»

- Убедитесь, что Docker запущен.
- Проверьте, что контейнер поднялся: `docker ps`.
- Посмотрите логи контейнера: `docker-compose -f docker-compose.test.yml logs`.

### Порт 5433 уже занят

Измените порт в `docker-compose.test.yml` (например, на `5434:5432`) и соответствующим образом поправьте `TEST_DATABASE_URL` в `tests/conftest.py`.

### Ошибка импорта модулей (ModuleNotFoundError)

Все тесты должны запускаться из директории `backend`. Убедитесь, что вы находитесь в ней перед запуском pytest.

### Предупреждения о кодировке или UnicodeDecodeError

Возникают при неправильном пароле или параметрах подключения. Проверьте `tests/conftest.py`: в `TEST_DATABASE_URL` не должно быть кириллицы или спецсимволов.

### Ошибка «IntegrityError» и последующие тесты падают

Тесты, проверяющие уникальность, должны после ожидаемой ошибки вызывать `db_session.rollback()`. В текущей версии тестов это уже реализовано.

---

## 8. Покрытие кода

Ниже приведены минимальные целевые показатели покрытия (согласно заданию):

| Модуль              | Целевое покрытие |
|---------------------|------------------|
| `models/`           | 100%             |
| `core/config.py`    | 100%             |
| `core/database.py`  | 100%             |
| `api/endpoints/`    | ≥ 90%            |
| `services/`         | ≥ 90%            |

Текущее покрытие можно посмотреть после выполнения `pytest --cov=app --cov-report=term`.

---

## 9. Интеграция в CI/CD (пример для GitHub Actions)

```yaml
- name: Run backend tests
  run: |
    cd backend
    docker-compose -f docker-compose.test.yml up -d
    sleep 5
    pip install -r requirements.txt
    pip install pytest pytest-cov
    pytest -v --cov=app --cov-report=xml
    docker-compose -f docker-compose.test.yml down
```

---

Готово. После выполнения этих шагов вы получите полностью рабочее тестовое окружение.  
При возникновении вопросов обращайтесь к документации pytest или к README проекта.