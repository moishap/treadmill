"""Unit test for endpoint websocket API.
"""

import unittest

import jsonschema

from treadmill.websocket.api import endpoint


class WSEndpointAPITest(unittest.TestCase):
    """Tests for endpoint websocket API."""

    def test_subscribe(self):
        """Test subscription registration."""
        api = endpoint.EndpointAPI()
        self.assertEquals(
            [('/endpoints/foo', 'bar#*:tcp:http')],
            api.subscribe({'topic': '/endpoints',
                           'filter': 'foo.bar',
                           'proto': 'tcp',
                           'endpoint': 'http'})
        )

        self.assertEquals(
            [('/endpoints/foo', '*#*:*:*')],
            api.subscribe({'topic': '/endpoints',
                           'filter': 'foo.*',
                           'proto': '*',
                           'endpoint': '*'})
        )

        self.assertEquals(
            [('/endpoints/foo', '*#*:*:*')],
            api.subscribe({'topic': '/endpoints',
                           'filter': 'foo.*'})
        )

        self.assertEquals(
            [('/endpoints/foo', '[t]?*#*:tcp:http')],
            api.subscribe({'topic': '/endpoints',
                           'filter': 'foo.[t]?*',
                           'proto': 'tcp',
                           'endpoint': 'http'})
        )

        with self.assertRaisesRegexp(
            jsonschema.exceptions.ValidationError,
            "'foo!' does not match"
        ):
            api.subscribe({'topic': '/endpoints',
                           'filter': 'foo!',
                           'proto': 'tcp',
                           'endpoint': 'http'})

        with self.assertRaisesRegexp(
            jsonschema.exceptions.ValidationError,
            "'endpoint_name' was unexpected"
        ):
            api.subscribe({'topic': '/endpoints',
                           'filter': 'foo.*',
                           'proto': 'tcp',
                           'endpoint_name': 'http'})

        with self.assertRaisesRegexp(
            jsonschema.exceptions.ValidationError,
            "None is not of type 'string'"
        ):
            api.subscribe({'topic': '/endpoints',
                           'filter': 'foo.*',
                           'proto': None,
                           'endpoint': None})

    def test_on_event(self):
        """Tests payload generation."""
        api = endpoint.EndpointAPI()
        self.assertEquals(
            {'endpoint': 'http',
             'name': 'foo.bar#1234',
             'proto': 'tcp',
             'topic': '/endpoints',
             'host': 'xxx',
             'sow': True,
             'port': '1234'},
            api.on_event(
                '/endpoints/foo/bar#1234:tcp:http',
                None,
                'xxx:1234'
            )
        )

        self.assertEquals(
            {'endpoint': 'http',
             'name': 'foo.bar#1234',
             'proto': 'tcp',
             'topic': '/endpoints',
             'host': 'xxx',
             'sow': False,
             'port': '1234'},
            api.on_event(
                '/endpoints/foo/bar#1234:tcp:http',
                'm',
                'xxx:1234'
            )
        )

        self.assertEquals(
            {'endpoint': 'http',
             'name': 'foo.bar#1234',
             'proto': 'tcp',
             'topic': '/endpoints',
             'host': None,
             'sow': False,
             'port': None},
            api.on_event(
                '/endpoints/foo/bar#1234:tcp:http',
                'd',
                None
            )
        )

        self.assertIsNotNone(
            api.on_event(
                '/endpoints/foo/bar#1234:tcp:http',
                'c',
                'xxx:1234'
            )
        )


if __name__ == '__main__':
    unittest.main()