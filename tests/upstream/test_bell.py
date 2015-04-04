import unittest

from ringing import Bell


class BellTest(unittest.TestCase):
    def test_bell(self):
        self.assertEqual(Bell(), 0)
        self.assertEqual(Bell(4), 4)
        self.assertEqual(Bell(Bell.MAX_BELLS), Bell.MAX_BELLS)

    def test_bell_from_char(self):
        self.assertEqual(Bell('5'), 4)
        self.assertEqual(Bell('0'), 9)
        self.assertEqual(Bell('T'), 11)

        # Should this be a custom excption?
        self.assertRaises(ValueError, lambda: Bell('%'))

    def test_bell_to_char(self):
        self.assertEqual(Bell(5).to_char(), '6')
        self.assertEqual(Bell(10).to_char(), 'E')
        self.assertEqual(Bell(14).to_char(), 'C')
        self.assertEqual(Bell(Bell.MAX_BELLS).to_char(), '*')

    def test_bell_output(self):
        s = '{}{}{}'.format(Bell(5), Bell(12), Bell(Bell.MAX_BELLS))
        expected = '6A{' + str(Bell.MAX_BELLS + 1) + '}'
        self.assertEqual(s, expected)
