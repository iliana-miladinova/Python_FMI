import unittest
from secret import validate_recipe, RuinedNikuldenDinnerError
from unittest.mock import patch, mock_open

class TestNikuldenValidator(unittest.TestCase):
    def test_valid_recipe(self):
        VALID_FILE_DATA = "Супа от рибена глава със сьонга"
        m = mock_open(read_data=VALID_FILE_DATA)
        with patch("builtins.open", m):
            result = validate_recipe("valid_fish_recipe.txt")
        self.assertTrue(result)

    def test_invalid_recipe(self):
        INVALID_FILE_DATA = "Пица пеперони"
        m = mock_open(read_data=INVALID_FILE_DATA)
        with patch("builtins.open", m):
            result = validate_recipe("invalid_fish_recipe.txt")
        self.assertFalse(result)

    def test_bad_recipe_file(self):
        with patch("builtins.open", side_effect=OSError):
            with self.assertRaises(RuinedNikuldenDinnerError):
                validate_recipe("fish_recipe.txt")

        FILE_DATA = "Супа от рибена глава със сьонга"
        m = mock_open(read_data=FILE_DATA)
        with patch("builtins.open", m) as mock_file:
            mock_file.return_value.read.side_effect = IOError
            with self.assertRaises(RuinedNikuldenDinnerError):
                validate_recipe("fish_recipe.txt")


if __name__ == "__main__":
    unittest.main()