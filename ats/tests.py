from django.test import TestCase
from .models import *
# Create your tests here.

class ATS_views_test_case(TestCase):

    def test_index(self):
            resp = self.client.get('') #index url
            self.assertEqual(resp.status_code, 200)
            self.assertTrue('latest_candidate_list' in resp.context)
            self.assertEqual([candidate.pk for candidate in resp.context['latest_candidate_list']], [1])
