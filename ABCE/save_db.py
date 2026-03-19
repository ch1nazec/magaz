# save_db.py
import os
import django
import json
from django.core import serializers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ABCE.settings')
django.setup()

from django.apps import apps

# Собираем все данные
all_data = []
for model in apps.get_models():
    if model._meta.app_label not in ['admin', 'auth', 'contenttypes', 'sessions']:
        queryset = model.objects.all()
        if queryset.exists():
            all_data.extend(serializers.serialize('json', queryset))

# Сохраняем в UTF-8
with open('full_db.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

print(f'✅ Сохранено {len(all_data)} записей в full_db.json')