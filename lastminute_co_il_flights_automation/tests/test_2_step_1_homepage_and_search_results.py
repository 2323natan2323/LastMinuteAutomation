import pytest
from playwright.sync_api import sync_playwright
from datetime import date, timedelta


from lastminute_co_il_flights_automation.pages.page1_home_page import HomePage
from lastminute_co_il_flights_automation.pages.page2_search_results_page import \
    SearchResultsPage
from lastminute_co_il_flights_automation.tests.base_test import BaseTest

class TestHomepageSearch(BaseTest):

    def test_homepage_and_search_results(self, page):

        page.goto("https://test.lastminute.co.il/")

        # 2. Home Page
        self.home = HomePage(page)
        self.home.handle_prompt_and_assert_login("LMT2024")
        self.home.safe_landing()
        self.home.close_cookies_message()
        self.home.click_flight_tab()
        self.home.set_trip_direction()
        self.home.set_passenger_type_and_count()
        self.home.set_flight_class()
        self.home.choose_outbound_flight("תל אביב")
        self.home.choose_inbound_flight("אתונה")
        self.home.set_flight_dates("22", "29")

        self.search = SearchResultsPage(page)

        self.search.set_fallback_params({
            "outbound_city_fallback_param": "תל אביב",
            "inbound_city_fallback_param": "לרנקה",

            "outbound_flight_1_date": "12",
            "inbound_flight_1_date": "19",

            "outbound_flight_2_date": "13",
            "inbound_flight_2_date": "20",

            "outbound_flight_3_date": "16",
            "inbound_flight_3_date": "23",

            "outbound_flight_4_date": "18",
            "inbound_flight_4_date": "25",

            "outbound_flight_5_date": "21",
            "inbound_flight_5_date": "28",
        })

        # fallback מתבצע כולו בתוך הקלאס של העמוד
        success = self.search.retry_search_with_alternative_dates()

        if not success:
            raise Exception("❌ No valid flight dates found, aborting test.")

        self.search.check_el_al_airways_airline_filter()
        self.search.click_more_flight_button_up_to_six_times()
        new_tab = self.search.choose_el_al_airways_flight()

