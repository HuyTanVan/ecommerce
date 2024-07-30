from django.test import TestCase
from django.urls import reverse
from ecommerce.apps.store.models import *
class TestCategoryModels(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="laptop", slug='laptop', is_active=True)
    def test_category_type(self):
        self.assertIsInstance(self.category, Category)
        
