"""Tests for the :mod:`references.controllers.health` module."""

import unittest
from unittest import mock
from references.controllers.health import health_check


class TestHealthCheck(unittest.TestCase):
    @mock.patch('references.controllers.health.cermine')
    @mock.patch('references.controllers.health.referencesStore')
    @mock.patch('references.controllers.health.extractionEvents')
    @mock.patch('references.controllers.health.grobid')
    @mock.patch('references.controllers.health.metrics')
    @mock.patch('references.controllers.health.refExtract')
    def test_health_check_ok(self, *mocks):
        """A dict of health states is returned."""
        status = health_check()
        self.assertIsInstance(status, dict)
        self.assertEqual(len(status), 6)
        for stat in status.values():
            self.assertTrue(stat)

    @mock.patch('references.controllers.health.cermine')
    @mock.patch('references.controllers.health.referencesStore')
    @mock.patch('references.controllers.health.extractionEvents')
    @mock.patch('references.controllers.health.grobid')
    @mock.patch('references.controllers.health.metrics')
    @mock.patch('references.controllers.health.refExtract')
    def test_health_check_failure(self, *mocks):
        """A dict of health states is returned."""
        for obj in mocks:
            print(obj)
            type(obj).session = mock.PropertyMock(side_effect=RuntimeError)

        status = health_check()
        self.assertIsInstance(status, dict)
        self.assertEqual(len(status), 6)
        print(status)
        for stat in status.values():
            self.assertFalse(stat)
