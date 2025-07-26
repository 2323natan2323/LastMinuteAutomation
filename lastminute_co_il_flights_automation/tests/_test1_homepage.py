import pytest
from playwright.sync_api import sync_playwright

from lastminute_co_il_flights_automation.tests.base_test import BaseTest
from lastminute_co_il_flights_automation.pages.page1_home_page import HomePage

class TestFlightBooking(BaseTest):

    def test_homepage(self, page):

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

