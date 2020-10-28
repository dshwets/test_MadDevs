from django.test import TestCase

from history_service.models import Links
from history_service.views import PER_PAGE, CommitSaver


class CommitSaverTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Links.objects.create(link='https://github.com/dshwets/New_Shop')
        Links.objects.create(link='https://gitlab.com/utopia-planitia/cassandra')

    def test_link_github(self):
        link_obj = Links.objects.first()
        api_path = CommitSaver(link_obj)._make_api_path()
        self.assertEqual(api_path, 'https://api.github.com/repos/dshwets/New_Shop/commits?per_page=' + PER_PAGE)

    def test_link_gitlab(self):
        link_obj = Links.objects.last()
        api_path = CommitSaver(link_obj)._make_api_path()
        self.assertEqual(api_path,
                         'https://gitlab.com/api/v4/projects/utopia-planitia%2Fcassandra/repository/commits?per_page='
                         + PER_PAGE)

    def test_make_request(self):
        link_obj = Links.objects.first()
        responses = CommitSaver(link_obj)._make_request()
        for response in responses:
            self.assertEqual(str(type(response)), "<class 'list'>")
            self.assertTrue(len(response) > 0)
