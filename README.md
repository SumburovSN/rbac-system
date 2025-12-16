RBAC (Role Based Access Control)
Таблицы реализованы в sqlite и в postgres (при наличии .env - пример example.env)
Структура данных:
1. Пользователи(id, email, имя, is_active-для мягкого удаления)
2. Роли (id, наименование, описание)
3. Бизнес-элементы (id, код, наименование) 
4. Правила для ролей (id, id роли, id бизнес-элемента, read_permission, create_permission, update_permission, delete_permission) 
5. Назначение ролей пользователям (id, id пользователя, id роли)

Система аутентификации настроена следующим образом:
1. Login: Создается объект сессии с uuid
2. Создается jwt token, который включает uuid сессии
3. jwt token отправляется пользователю в виде cookies

Начать в Swagger можно, используя данные "Superadmin", email: "superadmin@example.com", password: "admin".
Таблицы инициализируются значениями, которые можно посмотреть в app/infrastructure/db/init_db.py.

Все endpoints проверяют полномочия на соответствующее действие, за исключением:
1. Регистрация пользователя
2. Логин пользователя

Доступ к бизнес-элементу осуществляется с проверкой наименования бизнес-элемента (за исключением элемента "all"),
а также полномочия. Пользователю даются полномочия read, update, delete своего аккаунта (по user_id) 

Приложение на основе FastAPI
ЗАПУСК из корневой папки: uvicorn app.main:app --reload
Переадресация  http://127.0.0.1:8000 сразу на Swagger

Для работы приложения требуется запуск сервера Redis. Например, на Ubuntu установка Valkey-server (fork Redis): 
- sudo apt install redis-tools
- sudo apt install valkey-redis-compat
Запуск:
- sudo systemctl start valkey
- sudo systemctl status valkey
Проверка:
- redis-cli ping
Потребовалось удаление файла миграции:
- sudo rm /etc/valkey/REDIS_MIGRATION
Перезапуск:
- sudo systemctl restart valkey-server


alembic запускать из директории app:
alembic revision --autogenerate -m "initial schema"
alembic upgrade head

Не реализованы (продолжаю работать над):
1. Тесты
2. Проверка наличия базы данных rbac_api в postgres и ее создание при отсутствии  


