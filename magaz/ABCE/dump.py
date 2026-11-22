import os
import django
import json
from django.core import serializers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ABCE.settings')
django.setup()

# Собираем все данные
from django.apps import apps

all_data = []
for model in apps.get_models():
    if model._meta.app_label not in ['admin', 'auth', 'contenttypes', 'sessions']:
        queryset = model.objects.all()
        if queryset.exists():
            data = serializers.serialize('json', queryset)
            all_data.extend(json.loads(data))

# Сохраняем напрямую в файл
with open('all_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

print(f'✅ Сохранено {len(all_data)} записей в all_data.json')