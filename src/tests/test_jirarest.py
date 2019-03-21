import unittest
from unittest import mock
from src.main import jirarest

base = "http://localhost:8080"


class MyTestCase(unittest.TestCase):

    def test_ServerObject(self):
        server = jirarest.Server(base)

        self.assertIsNotNone(server)

    def test_ServerURI(self):
        server = jirarest.Server(base)

        self.assertIsNotNone(server.uri())
        self.assertEqual(server.uri(), base + "/rest/api/2")

    def test_ServerLatestURI(self):
        server = jirarest.Server(base, use_latest=True)
        self.assertEqual(server.uri(), base + "/rest/api/latest")

    def test_ServerChangeBaseURL(self):
        server = jirarest.Server(base)
        self.assertEqual(server.uri(), base + "/rest/api/2")

        new_base = "https://jira.atlassian.com"
        server.change_base_url(new_base)
        self.assertEqual(server.uri(), new_base + "/rest/api/2")

    @mock.patch('builtins.print')
    def test_generate_rest(self, mock_print):
        resource = "/project"
        server = jirarest.Server(base, 'fparan', 'password')

        test = server.generate_rest(resource)

        self.assertEqual(test, server.uri() + resource)
        self.assertFalse(mock_print.called)

        test = server.generate_rest('/issues', verbose=True)

        self.assertNotEqual(test, server.uri() + resource)
        self.assertEqual(test, server.uri() + '/issues')
        self.assertTrue(mock_print.called)

    @mock.patch('src.main.jirarest.Server.generate_rest')
    @mock.patch('src.main.jirarest.requests.get')
    def test_ServerGETOperation(self, mock_get, mock_generate_rest):
        get_resource = "/project"
        server = jirarest.Server(base, 'fparan', 'password')

        server.get_operation(get_resource)
        self.assertTrue(mock_get.called)
        self.assertTrue(mock_generate_rest.called)

    @mock.patch('src.main.jirarest.Server.get_operation')
    def test_ServerGETProjects(self, mock_get_operation):
        server = jirarest.Server(base)
        server.get_projects()

        self.assertTrue(mock_get_operation.called)

    @mock.patch('src.main.jirarest.Server.get_operation')
    def test_ServerGETProjectsKeyValue(self, mock_get_operation):
        server = jirarest.Server(base)
        mock_get_operation.return_value = [
            {"name": "foo",  'key': "FOO",  "id": "123",  'expand': 'description,lead,url,projectKeys'},
            {"name": "bar",  'key': "BAR",  "id": "456",  'expand': 'description,lead,url,projectKeys'},
            {"name": "blah", 'key': "BLAH", "id": "789",  'expand': 'description,lead,url,projectKeys'}]

        result = server.get_projects(get_keys=['name','id'])
        expected = [
            {"name": "foo",  "id": "123"},
            {"name": "bar",  "id": "456"},
            {"name": "blah", "id": "789"}]

        self.assertTrue(mock_get_operation.called)
        self.assertEqual(result, expected)

        result = server.get_projects(get_keys=['name'])
        expected = [
            {"name": "foo"},
            {"name": "bar"},
            {"name": "blah"}]

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
