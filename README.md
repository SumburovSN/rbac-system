RBAC (Role Based Access Control)
Таблицы реализованы в sqlite
Структура данных:
1. Пользователи(id, email, имя, is_active-для мягкого удаления)
2. Роли (id, наименование, описание)
3. Бизнес-элементы (id, код, наименование) 
4. Правила для ролей (id, id роли, id бизнес-элемента, read_permission, create_permission, update_permission, delete_permission) 
5. Назначение ролей пользователям (id, id пользователя, id роли)

База данных инициализируется данными:
Пользователи:
        ("Superadmin", "superadmin@example.com", "admin")
        ("Access Admin", "access.admin@example.com", "access123")
        ("Warehouse Manager", "warehouse.manager@example.com", "whmanager")
        ("Warehouse Viewer", "warehouse.viewer@example.com", "whviewer")
        ("Procurement Manager", "procurement.manager@example.com", "procmanager")
        ("Procurement Viewer", "procurement.viewer@example.com", "procviewer")
        ("Auditor", "auditor@example.com", "audit123")
Бизнес-элементы
        ("all", "Все базы данных"),
        ("users", "Список пользователей"),
        ("business_elements", "Блоки приложения для доступа"),
        ("roles", "Пользовательские роли"),
        ("access_role_rules", "Правила доступа роли к блоку приложения"),
        ("user_roles", "Назначение роли (предоставление права доступа к блоку приложения"),
        ("goods", "Склад, получение товаров и распределение их по магазинам"),
        ("orders", "Заказ товаров и работа с поставщиками"),
    
Роли:
        ("Superadmin", "Администратор базы данных (полный доступ ко всем таблицам и ролям)")
        ("AccessAdmin", "Администратор прав доступа (может управлять пользователями и ролями)")
        ("WarehouseManager", "Менеджер склада (полный доступ к товарам на складе)")
        ("WarehouseViewer", "Просмотр склада (только чтение товаров)")
        ("ProcurementManager", "Менеджер закупок (полный CRUD по заказам)")
        ("ProcurementViewer", "Просмотр заказов (только чтение)")
        ("Auditor", "Аудитор (чтение всех данных без возможности изменения)")
Правила для ролей:
        ("Superadmin", "all", True, True, True, True)        
        ("AccessAdmin", "users", True, True, True, True),
        ("AccessAdmin", "user_roles", True, True, True, True),
        ("AccessAdmin", "business_elements", True, True, True, True),
        ("AccessAdmin", "access_role_rules", True, True, True, True),
        ("WarehouseManager", "goods", True, True, True, True),        
        ("ProcurementManager", "orders", True, True, True, True),        
        ("WarehouseViewer", "goods", True, False, False, False),
        ("ProcurementViewer", "orders", True, False, False, False),
        ("Auditor", "goods", True, False, False, False),
        ("Auditor", "orders", True, False, False, False)
Роли распределяются по пользователям соответствующим образом.

Все endpoints проверяют полномочия на соответствующее действие, за исключением:
1. Регистрация пользователя
2. Логин пользователя

Доступ к бизнес-элементу осуществляется с проверкой наименования бизнес-элемента (за исключением элемента "all"),
а также полномочия. Пользователю даются полномочия read, update, delete своего аккаунта (по user_id) 

Приложение на основе FastAPI
ЗАПУСК: uvicorn app.main:app --reload
Переадресация  http://127.0.0.1:8000 сразу на Swagger
В Swagger сначала эндпоинт логин, например: email "superadmin@example.com", password: "admin" - получаем JWT токен
Затем в Swagger идем вверх, справа жмем кнопку AUTHORIZE и вводим токен в HTTPBearer  (http, Bearer) Value.

Для работы приложения (именно blacklist logout) требуется запуск сервера Redis. 

Не реализованы (продолжаю работать над):
1. Репозиторий под postgesql


