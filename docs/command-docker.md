# Посмотреть статус контейнеров
docker ps

# Посмотреть логи приложения (в реальном времени)
docker compose -f docker-compose.prod.yml logs -f app

# Остановить всё
docker compose -f docker-compose.prod.yml down

# Перезапустить после изменений в коде
docker compose -f docker-compose.prod.yml restart app

# Войти в контейнер приложения (для отладки)
docker exec -it task_flow_app bash

# Войти в базу данных
docker exec -it task_flow_db psql -U task_user -d task_flow

# Остановить и удалить всё (включая данные БД)
docker compose -f docker-compose.prod.yml down -v