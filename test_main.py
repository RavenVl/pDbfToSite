import unittest
from main import group_name_from_marki
class TestNameFromGoups(unittest.TestCase):

    def test_first_naim(self):
        self.assertEqual('КОМПЛЕКТУЮЩИЕ МЕТАН', group_name_from_marki('7'))

    def test_two_group(self):
        self.assertEqual(group_name_from_marki('21'), 'БАЛЛОН > БАЛЛОН БЫТОВОЙ')

    def test_three_group(self):
        self.assertEqual(group_name_from_marki('28'), 'ЕВРОПА > ЕВРОПА/МИНИКИТ/ЭЛЕКТРОН. > МИНИКИТ/DIGITRONIC')

if __name__ == '__main__':
    unittest.main()