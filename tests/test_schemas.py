import unittest

from pydantic import ValidationError

from app.schemas import SimpleHouseInput


class SimpleHouseInputValidationTests(unittest.TestCase):
    def base_kwargs(self, **overrides):
        kwargs = {
            "total_area": 2000,
            "lot_area": 5000,
            "totrmsabvgrd": 7,
            "bedroomabvgr": 3,
            "overallqual": 7,
            "house_age": 20,
            "garagecars": 2,
            "fireplaces": 1,
            "neighborhood": "CollgCr",
        }
        kwargs.update(overrides)
        return kwargs

    def test_rejects_overallqual_above_10(self):
        with self.assertRaises(ValidationError):
            SimpleHouseInput(**self.base_kwargs(overallqual=11))

    def test_rejects_overallqual_below_1(self):
        with self.assertRaises(ValidationError):
            SimpleHouseInput(**self.base_kwargs(overallqual=0))

    def test_accepts_overallqual_in_range(self):
        for value in (1, 7, 10):
            model = SimpleHouseInput(**self.base_kwargs(overallqual=value))
            self.assertEqual(model.overallqual, value)

    def test_rejects_negative_bedrooms(self):
        with self.assertRaises(ValidationError):
            SimpleHouseInput(**self.base_kwargs(bedroomabvgr=-1))

    def test_rejects_non_positive_lot_area(self):
        with self.assertRaises(ValidationError):
            SimpleHouseInput(**self.base_kwargs(lot_area=0))


if __name__ == "__main__":
    unittest.main()
