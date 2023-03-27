"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as PsycopgOp2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# Those patches are the arguments from the class functions(i.e patched_check)
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready"""
        # When mocking an object, we simply return true
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""
        # As we want to raise exceptions that would be
        # raised if the database wasn't ready, we use the side_effect
        # because it allows us to pass in various different items
        # that get handled differently depending on the time.
        # (if we pass an exception, mocking library knows
        # it should raise the exception)
        patched_check.side_effect = [PsycopgOp2Error] * 2 + \
            [OperationalError] * 3 + [True]
        # In this case, we are saying that the first two times we call
        # the mocked method, we raise the psycopg2error, and the next 3 times
        # we raise an operationalError. After those 5 calls, it returns True

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
