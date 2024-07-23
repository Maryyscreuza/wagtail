from django.core.exceptions import ValidationError
from django.test import TestCase
from wagtail.models import Collection
from wagtail.admin.forms.collections import CollectionForm 

class CollectionFormTest(TestCase):

    def setUp(self):
        self.collection = Collection.objects.create(name="Test Collection")
        self.parent_collection = Collection.objects.create(name="Parent Collection")
        self.child_collection = Collection.objects.create(name="Child Collection", parent=self.collection)

    def test_instance_in_edit_mode_with_modified_parent(self):
        # CT1: Instância em Modo de Edição com Parent Modificado
        # Entrada
        form_data = {
            'name': 'Test Collection',
            'parent': self.parent_collection.pk
        }
        form = CollectionForm(data=form_data, instance=self.collection, initial={'parent': self.collection.pk})
        
        # Saída Esperada: O bloco dentro do `if` é executado, e se `parent.pk` estiver em `old_descendants`, uma `ValidationError` é levantada.
        self.assertFalse(form.is_valid())
        self.assertIn('parent', form.errors)
        
    def test_instance_in_edit_mode_with_unmodified_parent(self):
        # CT2: Instância em Modo de Edição com Parent Não Modificado
        # Entrada
        form_data = {
            'name': 'Test Collection',
            'parent': self.collection.pk
        }
        form = CollectionForm(data=form_data, instance=self.collection, initial={'parent': self.collection.pk})
        
        # Saída Esperada: O bloco dentro do `if` não é executado.
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['parent'], self.collection)

    def test_instance_in_add_mode_with_modified_parent(self):
        # CT3: Instância em Modo de Adição com Parent Modificado
        # Entrada
        new_collection = Collection(name="New Collection")
        form_data = {
            'name': 'New Collection',
            'parent': self.parent_collection.pk
        }
        form = CollectionForm(data=form_data, instance=new_collection, initial={'parent': self.collection.pk})
        
        # Saída Esperada: O bloco dentro do `if` não é executado.
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['parent'], self.parent_collection)
