from django.core.cache import cache
from django.test import TestCase
import mock


class MixerTests(TestCase):
    def tearDown(self):
        cache.clear()

    @mock.patch('mixer.views.parse')
    def test_add_feed(self, mock_parse):
        mock_parse.return_value.entries = 'entries'
        mock_parse.return_value.feed.link = 'link'
        mock_parse.return_value.feed.title = 'title'

        response = self.client.post('/', {'url': 'http://example.com'})
        self.assertIn('items', cache)
        self.assertIn('entries', cache.get('items').values())
        self.assertIn('feeds', cache)
        self.assertIn('link', cache.get('feeds').values())

    def test_remove_feed(self):
        cache.set('feeds', {'title': 'link', 'another-title': 'link'})
        cache.set('items', {'title': ['item'], 'another-title': ['item']})

        response = self.client.get('/delete/title')

        self.assertNotIn('title', cache.get('feeds'))
        self.assertNotIn('title', cache.get('items'))
