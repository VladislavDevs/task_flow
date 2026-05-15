## 🐳 Запуск с Docker

### Продакшен окружение

1. Убедитесь, что Docker Desktop установлен и запущен

2. Скопируйте и настройте переменные окружения:
   ```bash
   cp .env.example .env
   # Отредактируйте .env, установите SECRET_KEY

3. Запустите все:
```bash
docker compose -f docker-compose.prod.yml up -d
```

4. API доступно: http://localhost:8000

5. Документация: http://localhost:8000/docs

6. PgAdmin (опционально): http://localhost:5050

* Логин: admin@taskflow.com

* Пароль: admin

ОСТАНОВКА
```bash
docker compose -f docker-compose.prod.yml down
```