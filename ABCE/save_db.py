# save_db.py
import os
import django
import json
from django.core import serializers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ABCE.settings')
django.setup()

from django.apps import apps
from products.models import Category


for c in Category.objects.all():
    print(c.image.name)