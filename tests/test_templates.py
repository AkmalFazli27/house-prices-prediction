import unittest
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "app" / "templates"


class TemplateRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.environment = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    def render_result(self, prediction=None, confidence=None, lower=None,
                      upper=None, error=None):
        template = self.environment.from_string(
            "{% from 'components/result_banner.html' import result_banner %}"
            "{{ result_banner(prediction, confidence, lower, upper, error) }}"
        )
        return template.render(
            prediction=prediction,
            confidence=confidence,
            lower=lower,
            upper=upper,
            error=error,
        )

    def test_initial_result_banner_is_empty(self):
        self.assertEqual(
            self.render_result().strip(),
            "",
        )

    def test_prediction_result_uses_jinja_safe_formatting(self):
        html = self.render_result(
            prediction=250000.4,
            confidence=82,
            lower=225000,
            upper=275000,
        )

        self.assertIn("$250,000", html)
        self.assertIn("$225,000", html)
        self.assertIn("$275,000", html)
        self.assertIn("82%", html)

    def test_prediction_result_uses_stacked_mobile_layout(self):
        html = self.render_result(
            prediction=250000.4,
            confidence=82,
            lower=225000,
            upper=275000,
        )

        self.assertIn("grid-cols-1 sm:grid-cols-2", html)
        self.assertIn("p-6 sm:p-10", html)
        self.assertIn("gap-6 sm:gap-10", html)
        self.assertIn("min-w-0", html)
        self.assertIn("items-start sm:items-end", html)
        self.assertIn("text-left sm:text-right", html)

    def test_error_result_does_not_render_success_card(self):
        html = self.render_result(error="Prediction failed")

        self.assertIn("Prediction Error", html)
        self.assertIn("Prediction failed", html)
        self.assertNotIn("Estimated Sale Price", html)

    def test_navbar_restores_brand_and_active_page_accessibility(self):
        html = self.environment.get_template(
            "components/navbar.html"
        ).render(active_nav="simple")

        self.assertIn("Omah.AI", html)
        self.assertNotIn("House Prices", html)
        self.assertIn('href="/simple"', html)
        self.assertIn('aria-current="page"', html)
        self.assertIn("font-label", html)
        self.assertIn("uppercase", html)
        self.assertIn("border-b-2", html)

    def test_predict_button_contains_loading_state_markup(self):
        html = self.environment.from_string(
            "{% from 'components/btn_predict.html' import btn_predict %}"
            "{{ btn_predict() }}"
        ).render()

        self.assertIn("btn-predict", html)
        self.assertIn("btn-label", html)
        self.assertIn("btn-predict-icon", html)
        self.assertIn("btn-predict-spinner", html)
        self.assertIn("hidden animate-spin", html)
        self.assertIn("h-4 w-4", html)
        self.assertIn('width="16"', html)
        self.assertIn('height="16"', html)
        self.assertIn("disabled:opacity-60", html)
        self.assertIn("disabled:cursor-not-allowed", html)


if __name__ == "__main__":
    unittest.main()
