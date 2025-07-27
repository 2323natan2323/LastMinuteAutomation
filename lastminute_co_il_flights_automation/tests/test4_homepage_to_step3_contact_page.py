import pytest
from playwright.sync_api import sync_playwright

from lastminute_co_il_flights_automation.pages.page1_home_page import HomePage
from lastminute_co_il_flights_automation.pages.page2_search_results_page import \
    SearchResultsPage
from lastminute_co_il_flights_automation.pages.page3_flexi_page import FlexiPage
from lastminute_co_il_flights_automation.pages.page4_contact_page import ContactPage
from lastminute_co_il_flights_automation.tests.base_test import BaseTest


class TestFlightBooking(BaseTest):

    def test_home_to_step3_contact_page(self, page):

        # 1. Contact & Passenger data
        contact_first_name = "Test"
        contact_last_name = "Prod"
        email = "natan@lastminute.co.il"
        phone_number = "0527491280"
        birthday = "23111999"
        passenger_first = "Natan"
        passenger_last = "Shor"
        full_name = f"{passenger_first} {passenger_last}"
        gender = "זכר"
        passport_expiration_date = "10102030"
        passport_number = "456456456"

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
        self.search.click_more_flight_button_up_to_six_times()
        new_tab = self.flexi = self.search.choose_elal_flight()

        # 4. Flexi Page
        self.flexi = FlexiPage(new_tab)
        self.flexi.wait_for_page_to_load()
        self.flexi.choose_flexi_ticket()

        # 5. Contact Page
        self.contact = ContactPage(new_tab)
        self.contact.wait_for_contact_page_to_load()
        self.contact.fill_contact_info(contact_first_name, contact_last_name, email, email, phone_number)
        self.contact.fill_passenger_info(passenger_first, passenger_last, birthday)
        self.contact.fill_passport_and_nationality_fields(passport_number, passport_expiration_date)
        self.contact.add_outbound_baggage()
        self.contact.add_inbound_baggage()
        self.contact.continue_to_next_page_with_recovery(
            contact_first_name, contact_last_name,
            passenger_first, passenger_last,
            email, email,
            phone_number, birthday, passport_number, passport_expiration_date
        )
