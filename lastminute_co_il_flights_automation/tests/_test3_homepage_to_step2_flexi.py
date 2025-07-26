import pytest
from playwright.sync_api import sync_playwright

from lastminute_co_il_flights_automation.pages.page1_home_page import HomePage
from lastminute_co_il_flights_automation.pages.page2_search_results_page import \
    SearchResultsPage
from lastminute_co_il_flights_automation.pages.page3_flexi_page import FlexiPage
from lastminute_co_il_flights_automation.tests.base_test import BaseTest


class TestFlightBooking(BaseTest):
    def test_homepage_to_step2_flexi(self, page):

        contact_first_name = "Test"
        contact_last_name = "Prod"
        email = "natan@lastminute.co.il"
        confirmation_email = "natan@lastminute.co.il"
        phone_number = "0527491280"
        birthday_date = "23111999"
        passenger_first = "Natan"
        passenger_last = "Shor"
        passenger_full_name = f"{passenger_first} {passenger_last}"
        passenger_gender = "זכר"

        page.goto("https://test.lastminute.co.il/")


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

        # 3. Search Page
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

        self.search.check_elal_airline_filter()
        self.search.choose_elal_flight()
        new_tab = self.search.choose_elal_flight()

        # 4. Flexi Page
        self.flexi = FlexiPage(new_tab)
        self.flexi.wait_for_page_to_load()
        self.flexi.choose_flexi_ticket()


