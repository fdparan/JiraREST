import unittest
from unittest import mock
from src.main import jirarest

base = "http://localhost:8080"


class MyTestCase(unittest.TestCase):
    def test_ServerURI(self):
        server = jirarest.Server(base)

        self.assertIsNotNone(server.uri)
        self.assertEqual(server.uri, base + "/rest/api/2")

    def test_ServerLatestURI(self):
        server = jirarest.Server(base, use_latest=True)
        self.assertEqual(server.uri, base + "/rest/api/latest")

    def test__uri(self):
        server = jirarest.Server(base)
        server._uri()

        self.assertEqual(server.uri, base + "/rest/api/2")

    def test_ServerChangeBaseURL(self):
        server = jirarest.Server(base)

        self.assertEqual(server.uri, base + "/rest/api/2")

        new_base = "https://jira.atlassian.com"

        server.change_base_url(new_base)

        self.assertEqual(server.uri, new_base + "/rest/api/2")

    @mock.patch('builtins.print')
    def test__rest_call(self, mock_print):
        resource = "/project"
        server = jirarest.Server(base, 'fparan', 'password')

        test = server._rest_call(resource)

        self.assertEqual(test, server.uri + resource)
        self.assertFalse(mock_print.called)

        test = server._rest_call('/issues', verbose=True)

        self.assertNotEqual(test, server.uri + resource)
        self.assertEqual(test, server.uri + '/issues')
        self.assertTrue(mock_print.called)

    @mock.patch('src.main.jirarest.Server._rest_call')
    @mock.patch('src.main.jirarest.requests.get')
    def test_ServerGETOperation(self, mock_get, mock__rest_call):
        get_resource = "/project"
        server = jirarest.Server(base, 'fparan', 'password')

        server.get_operation(get_resource)
        self.assertTrue(mock_get.called)
        self.assertTrue(mock__rest_call.called)

    @mock.patch('src.main.jirarest.Server.get_operation')
    def test_ServerGETProjects(self, mock_get_operation):
        server = jirarest.Server(base)
        server.get_projects()

        self.assertTrue(mock_get_operation.called)

if __name__ == '__main__':
    unittest.main()
