# Catalog-Ai

API для работы Catalog_AI_mobileapp.

API написано на FastAPI + SQLAlchemy из-за популярности такого стека.

В качестве базы данных для MVP была выбрана SQLite3 из-за своей простоты.

Для взаимодействия с ИИ использовался g4f.

Эндпоинты:
 - /api/v1/categories - возвращает все категории ИИ
 - /api/v1/ai/favorite/{user_id} - возвращает избранные юзером ИИ
 - /api/v1/ai/favorite - POST - добавляет ИИ в избранные; DELETE - удаляет ИИ из избранных
 - /api/v1/ai/{category} - возвращает ИИ категории category
 - /api/v1/ai/query - отправляет запрос ИИ
 - /api/v1/user/register - регистрация пользователя
 - /api/v1/user/login - авторизация пользователя
 - /api/v1/user/photo - смена аватарки пользователя