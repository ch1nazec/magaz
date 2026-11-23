# Django fixtures для ABCE

## Состав
- `products.json` — категории, бренды, марки/модели/поколения/модификации автомобилей, склады, товары, внешние артикулы, применяемость и остатки.
- `user.json` — демо-покупатель и демо-менеджер.
- `cart.json` — корзины и позиции.
- `order.json` — заказы и позиции заказов.

## Загрузка
В корне Django-проекта:

```bash
python manage.py migrate
python manage.py loaddata fixtures/products.json
python manage.py loaddata fixtures/user.json
python manage.py loaddata fixtures/cart.json
python manage.py loaddata fixtures/order.json
```

Или положите JSON-файлы в каталог `fixtures/` внутри соответствующих Django-приложений и выполните `python manage.py loaddata products user cart order`.

## Важно
1. Убедитесь, что в `settings.py` настроен `AUTH_USER_MODEL = "user.CustomUser"`.
2. Пароли демо-пользователей установлены как unusable (`!`). После загрузки задайте пароль через Django shell:
   ```python
   from user.models import CustomUser
   u = CustomUser.objects.get(email="ivan@example.com")
   u.set_password("DemoPass123!")
   u.save()
   ```
   Аналогично для `manager@example.com`.
3. `ProductImage` намеренно не включён: у ImageField нужны реальные локальные файлы. Остальные изображения/логотипы оставлены пустыми, так как соответствующие поля допускают пустое значение.
4. В `products.signals` обработчик Product обращается к Redis при загрузке fixture. Для `loaddata` Redis должен быть доступен; иначе временно отключите этот сигнал или добавьте в receiver проверку `if kwargs.get("raw"): return`.
5. Это демонстрационные данные, а не реальные остатки или цены.
