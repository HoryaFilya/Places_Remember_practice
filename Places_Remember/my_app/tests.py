from django.test import TestCase, Client
from django.urls import reverse
from my_app.models import Memory

class MemoryTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.memory_data = {
            'title': 'Test Memory',
            'comment': 'This is a test memory'
        }
        self.memory = Memory.objects.create(**self.memory_data)

    def test_memory_creation(self):
        self.assertEqual(Memory.objects.count(), 1)
        self.assertEqual(self.memory.title, self.memory_data['title'])
        self.assertEqual(self.memory.comment, self.memory_data['comment'])

    def test_add_memory_view(self):
        url = reverse('add_memory')
        response = self.client.post(url, self.memory_data)
        self.assertEqual(response.status_code, 302)

        memories = Memory.objects.all()
        self.assertEqual(memories.count(), 2)
        new_memory = memories.latest('id')
        self.assertEqual(new_memory.title, self.memory_data['title'])
        self.assertEqual(new_memory.comment, self.memory_data['comment'])