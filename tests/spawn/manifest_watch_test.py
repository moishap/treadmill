"""Unit test for treadmill.spawn.manifest_watch."""

import os
import unittest

import mock

import treadmill
from treadmill.spawn import manifest_watch


class ManifestWatchTest(unittest.TestCase):
    """Tests for teadmill.spawn.manifest_watch."""

    # Disable W0212: Access to a protected member
    # pylint: disable=W0212

    @mock.patch('os.chmod', mock.Mock())
    @mock.patch('treadmill.fs.mkdir_safe', mock.Mock())
    @mock.patch('os.path.exists', mock.Mock())
    def test_check_path(self):
        """Tests that the manifiest watch validates manifest filenames."""
        watch = manifest_watch.ManifestWatch('/does/not/exist', 2)

        os.path.exists.return_value = False

        self.assertFalse(watch._check_path('test.yml'))

        os.path.exists.return_value = True

        self.assertFalse(watch._check_path('.test.yml'))
        self.assertFalse(watch._check_path('test'))
        self.assertTrue(watch._check_path('test.yml'))

    @mock.patch("treadmill.spawn.manifest_watch.open", create=True)
    @mock.patch('os.path.exists', mock.Mock(return_value=False))
    @mock.patch('os.chmod', mock.Mock())
    @mock.patch('treadmill.fs.mkdir_safe', mock.Mock())
    @mock.patch('treadmill.fs.symlink_safe', mock.Mock())
    @mock.patch('treadmill.utils.create_script', mock.Mock())
    @mock.patch('treadmill.spawn.manifest_watch.ManifestWatch._scan',
                mock.Mock())
    def test_create_instance(self, mock_open):
        """Tests basic create instance functionality."""
        watch = manifest_watch.ManifestWatch('/does/not/exist', 2)

        watch._create_instance('test.yml')

        self.assertEquals(3, treadmill.fs.mkdir_safe.call_count)
        self.assertEquals(2, treadmill.utils.create_script.call_count)
        self.assertEquals(1, treadmill.fs.symlink_safe.call_count)
        self.assertEquals(2, mock_open.call_count)
        self.assertEquals(1, treadmill.spawn.manifest_watch.ManifestWatch
                          ._scan.call_count)

    @mock.patch('os.listdir', mock.Mock())
    @mock.patch('os.path.exists', mock.Mock(return_value=True))
    @mock.patch('os.chmod', mock.Mock())
    @mock.patch('treadmill.fs.mkdir_safe', mock.Mock())
    @mock.patch(
        'treadmill.spawn.manifest_watch.ManifestWatch._create_instance',
        mock.Mock())
    def test_sync(self):
        """Tests the initial sync of the manifests."""
        os.listdir.side_effect = [
            ['.test1.yml', 'test4.yml', 'what'],
        ]

        watch = manifest_watch.ManifestWatch('/does/not/exist', 2)
        watch.sync()

        treadmill.spawn.manifest_watch.ManifestWatch._create_instance \
                 .assert_called_with('/does/not/exist/manifest/test4.yml')


if __name__ == '__main__':
    unittest.main()