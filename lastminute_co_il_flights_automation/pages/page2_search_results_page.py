
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeout

from lastminute_co_il_flights_automation.pages.base_page import BasePage

class FlightData:
    def __init__(self):
        self.outbound_departure_time = None
        self.outbound_departure_date = None
        self.outbound_departure_iata_origin = None
        self.outbound_landing_time = None
        self.outbound_landing_date = None
        self.outbound_landing_iata_destination = None
        self.inbound_departure_time = None
        self.inbound_departure_date = None
        self.inbound_departure_iata_origin = None
        self.inbound_landing_time = None
        self.inbound_landing_date = None
        self.inbound_landing_iata_destination = None
        self.outbound_duration_time = None
        self.inbound_duration_time = None

class SearchResultsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._fallback_params = {}  # שלב 1: יצירת מקום לשמירת הפרמטרים
        self.saved_flight_data = FlightData()

    def save_el_al_airways_flight_details(self, segment):
        outbound_locator = segment.locator(self.SEGMENT_OUTBOUND_FLIGHT_TEXT)
        outbound_locator.wait_for(state="visible", timeout=10000)
        outbound_airline_name = outbound_locator.inner_text().strip().lower().replace("\n", "").replace("\t",
                                                                                                        "").replace(
            "  ", " ")

        inbound_locator = segment.locator(self.SEGMENT_INBOUND_FLIGHT_TEXT)
        inbound_locator.wait_for(state="visible", timeout=10000)
        inbound_airline_name = inbound_locator.inner_text().strip().lower().replace("\n", "").replace("\t", "").replace(
            "  ", " ")

        if "el al" in outbound_airline_name and "abcd" in inbound_airline_name:
            self.saved_flight_data.outbound_departure_time = segment.locator(
                self.FLIGHT_OUTBOUND_DEPARTURE_TIME).inner_text()
            self.saved_flight_data.outbound_departure_date = segment.locator(
                self.FLIGHT_OUTBOUND_DEPARTURE_DATE).inner_text()
            self.saved_flight_data.outbound_departure_iata_origin = segment.locator(
                self.FLIGHT_OUTBOUND_DEPARTURE_IATA_ORIGIN).inner_text()
            self.saved_flight_data.outbound_landing_time = segment.locator(
                self.FLIGHT_OUTBOUND_LANDING_TIME).inner_text()
            self.saved_flight_data.outbound_landing_date = segment.locator(
                self.FLIGHT_OUTBOUND_LANDING_DATE).inner_text()
            self.saved_flight_data.outbound_landing_iata_destination = segment.locator(
                self.FLIGHT_OUTBOUND_LANDING_IATA_DESTINATION).inner_text()
            self.saved_flight_data.inbound_departure_time = segment.locator(
                self.FLIGHT_INBOUND_DEPARTURE_TIME).inner_text()
            self.saved_flight_data.inbound_departure_date = segment.locator(
                self.FLIGHT_INBOUND_DEPARTURE_DATE).inner_text()
            self.saved_flight_data.inbound_departure_iata_origin = segment.locator(
                self.FLIGHT_INBOUND_DEPARTURE_IATA_ORIGIN).inner_text()
            self.saved_flight_data.inbound_landing_time = segment.locator(self.FLIGHT_INBOUND_LANDING_TIME).inner_text()
            self.saved_flight_data.inbound_landing_date = segment.locator(self.FLIGHT_INBOUND_LANDING_DATE).inner_text()
            self.saved_flight_data.inbound_landing_iata_destination = segment.locator(
                self.FLIGHT_INBOUND_LANDING_IATA_DESTINATION).inner_text()
            self.saved_flight_data.outbound_duration_time = segment.locator(self.FLIGHT_OUTBOUND_DURATION).inner_text()
            self.saved_flight_data.inbound_duration_time = segment.locator(self.FLIGHT_INBOUND_DURATION).inner_text()

    FLIGHT_CARD_LIST = ".results-page-body"
    SEARCH_RESULTS_VERIFY_ELEMENT = '.search-results-txt [key="Filter.SearchResults"]'
    NEW_SEARCH_RESULT_PAGE_ELEMENT = "app-flight-search-summary .search-summary"
    NEW_SEARCH_RESULT_DATE_PICKER = "app-datepicker .label-input"
    ELAL_FILTER_CHECK = '.right-section [value="LY"]'
    AVAILABLE_FLIGHTS_SEGMENTS = "app-flight-card .card-container"
    SEGMENT_OUTBOUND_FLIGHT_TEXT = ".flight-row:nth-child(1) .airline-box-name"
    SEGMENT_INBOUND_FLIGHT_TEXT = ".flight-row:nth-child(2) .airline-box-name"
    ORDER_FLIGHT_BTN = "app-flight-card-price-box .primary-btn"
    CHOOSE_FLIGHT_SEARCH_RESULTS_BTN = "app-flight-search-summary .search-summary-wrapper > .search-summary"
    DATE_PICKER = "app-datepicker .picker-container"
    NEXT_MONTH_BTN = "app-flight-search .month-item:nth-child(2) .button-next-month"
    FIND_ME_FLIGHTS_BTN = ".search-and-add-btn .primary-btn"
    CHOOSE_OUTBOUND_FLIGHT_BTN = ".destinations-container app-flights-autocomplete:nth-child(1) .input-wrapper"
    OUTBOUND_FLIGHT_CITY_TITLE = ".destinations-container app-flights-autocomplete:nth-child(1) .input-wrapper .text-input"
    ACTUAL_OUTBOUND_CITY = ".destinations-container app-flights-autocomplete:nth-child(1) .input-wrapper .option-item:nth-child(1) .main-text"
    CHOOSE_INBOUND_FLIGHT_BTN = ".destinations-container app-flights-autocomplete:nth-child(2) .input-wrapper"
    INBOUND_FLIGHT_CITY_TITLE = ".destinations-container app-flights-autocomplete:nth-child(2) .input-wrapper .text-input"
    ACTUAL_INBOUND_CITY = ".destinations-container app-flights-autocomplete:nth-child(2) .input-wrapper .option-item:nth-child(1) .main-text"
    SHOW_MORE_AIRLINES_BTN = "app-checkbox .show-more-btn"
    SHOW_MORE_FLIGHTS_BTN = ".card-wrapper .show-more-btn"

    FLIGHT_OUTBOUND_DEPARTURE_TIME = ".flight-row:nth-child(1) .destination-box:nth-child(1) .time"
    FLIGHT_OUTBOUND_DEPARTURE_DATE = ".flight-row:nth-child(1) .destination-box:nth-child(1) .date"
    FLIGHT_OUTBOUND_DEPARTURE_IATA_ORIGIN = ".flight-row:nth-child(1) .destination-box:nth-child(1)  .destination"
    FLIGHT_OUTBOUND_DURATION = ".flight-row:nth-child(1) .flight-details .time"

    FLIGHT_OUTBOUND_LANDING_TIME = ".flight-row:nth-child(1) .destination-box:nth-child(3) .time"
    FLIGHT_OUTBOUND_LANDING_DATE = ".flight-row:nth-child(1) .destination-box:nth-child(3) .date"
    FLIGHT_OUTBOUND_LANDING_IATA_DESTINATION = ".flight-row:nth-child(1) .destination-box:nth-child(3)  .destination"
    FLIGHT_INBOUND_DURATION = ".flight-row:nth-child(2) .flight-details .time"

    FLIGHT_INBOUND_DEPARTURE_TIME = ".flight-row:nth-child(2) .destination-box:nth-child(1) .time"
    FLIGHT_INBOUND_DEPARTURE_DATE = ".flight-row:nth-child(2) .destination-box:nth-child(1) .date"
    FLIGHT_INBOUND_DEPARTURE_IATA_ORIGIN = ".flight-row:nth-child(2) .destination-box:nth-child(1)  .destination"

    FLIGHT_INBOUND_LANDING_TIME = ".flight-row:nth-child(2) .destination-box:nth-child(3) .time"
    FLIGHT_INBOUND_LANDING_DATE = ".flight-row:nth-child(2) .destination-box:nth-child(3) .date"
    FLIGHT_INBOUND_LANDING_IATA_DESTINATION = ".flight-row:nth-child(2) .destination-box:nth-child(3) .destination"

    def set_fallback_params(self, params: dict):
        self._fallback_params = params  # שלב 2: קבלת הפרמטרים מקובץ הטסט


    def safe_load_search_results(self):
        """
        Ensures the search results page is loaded.
        If not, retries with alternative dates.
        """
        try:
            search_result_element = self._page.locator(self.SEARCH_RESULTS_VERIFY_ELEMENT)
            search_result_element.wait_for(state="visible", timeout=25000)
            print("✅ Search results page loaded successfully!")
        except PlaywrightTimeout:
            print("❌ Search results did not load in time. Trying alternative dates...")
            self.retry_search_with_alternative_dates()

    def retry_search_with_alternative_dates(self):
        print("🔁 Trying to reload search results or retry with alternate")

        # מוודאים אם תוצאות החיפוש הגיעו בכל זאת

        try:
            search_result_element = self._page.locator(self.SEARCH_RESULTS_VERIFY_ELEMENT)
            search_result_element.wait_for(state="visible", timeout=25000)
            print("✅ The search result page was loaded successfully!")

            return True

        except PlaywrightTimeout :
            print("❌ Search results not found, trying to select alternative dates")

            return self.alternative_flight_dates_1()

            #   לוחצים על כפתור בחירת טיסה מחדש

    def alternative_flight_dates_1(self):

        if self._page.is_closed():
            print("❌ Page has been closed, cannot proceed")
            return False

        new_search_result_element = self._page.locator(self.NEW_SEARCH_RESULT_PAGE_ELEMENT)
        new_search_result_element.wait_for(state="visible", timeout=10000)
        assert new_search_result_element.is_visible(), "❌ The new search result element is not visible!"
        self.click(self.NEW_SEARCH_RESULT_PAGE_ELEMENT)
        print("✅ The new search result element is visible!")

        # מוודאים שבורר התאריכים נפתח
        new_date_picker = self._page.locator(self.DATE_PICKER)
        new_date_picker.wait_for(state="visible", timeout=10000)
        assert new_date_picker.is_visible(), "❌ The new date picker is not visible!"
        self.click(new_date_picker)
        print("✅ Date picker opened.")

        next_month_btn = self._page.locator(self.NEXT_MONTH_BTN)
        next_month_btn.wait_for(state="visible", timeout=10000)
        self.click(next_month_btn)
        self.click(next_month_btn)
        self.click(next_month_btn)
        print("✅ Clicked on next month.")

        month_title = self._page.locator(".container__months .month-item:nth-child(1)  .month-item-name")
        month_name_text = self.get_inner_text(month_title)
        print(f"🕓 Current month title: {month_name_text}")

        outbound_flight_1_date = self._fallback_params.get("outbound_flight_1_date")
        outbound_flight_1 = self._page.locator('.container__months .month-item:nth-child(1) .container__days a.day-item').filter(has_text=f"{outbound_flight_1_date}")
        outbound_flight_1.wait_for(state="visible", timeout=10000)
        inbound_flight_1_date = self._fallback_params.get("inbound_flight_1_date")
        inbound_flight_1 = self._page.locator('.container__months .month-item:nth-child(1) .container__days a.day-item').filter(has_text=f"{inbound_flight_1_date}")
        inbound_flight_1.wait_for(state="visible", timeout=10000)

        if outbound_flight_1.is_visible() and inbound_flight_1.is_visible():
            print("✅ The flight route (13-20) is available, continue!")
            self.click(outbound_flight_1)
            self.click(inbound_flight_1)

            find_me_flight_btn = self._page.locator(self.FIND_ME_FLIGHTS_BTN)
            find_me_flight_btn.wait_for(state="visible", timeout=10000)
            assert find_me_flight_btn.is_visible(), "❌ Find me flights btn is not visible!"
            self.click(find_me_flight_btn)
            print("✅ Flight me flights btn was clicked successfully!")
            print("✅ Flight dates were set successfully!")

            try:
                search_result_element = self._page.locator(self.SEARCH_RESULTS_VERIFY_ELEMENT)
                search_result_element.wait_for(state="visible", timeout=25000)
                print("✅ The search result page was loaded successfully!")

                return True

            except PlaywrightTimeout:
                print("❌ Search results not found, trying to select alternative dates")
                return self.alternative_flight_dates_2()

        next_outbound_flight_2_date = self._fallback_params.get("outbound_flight_2_date", "?")
        next_inbound_flight_2_date = self._fallback_params.get("inbound_flight_2_date", "?")
        print(f"❌ The flight route ({outbound_flight_1_date}–{inbound_flight_1_date}) is not available, Trying alternative dates: {next_outbound_flight_2_date}-{next_inbound_flight_2_date}")

        return self.alternative_flight_dates_2()

    def alternative_flight_dates_2(self):

        new_search_result_element = self._page.locator(self.NEW_SEARCH_RESULT_PAGE_ELEMENT)
        new_search_result_element.wait_for(state="visible", timeout=10000)
        assert new_search_result_element.is_visible(), "❌ The new search result element is not visible!"
        self.click(new_search_result_element)
        print("✅ The new search result element is visible!")

        # מוודאים שבורר התאריכים נפתח
        new_date_picker = self._page.locator(self.DATE_PICKER)
        new_date_picker.wait_for(state="attached", timeout=10000)
        new_date_picker.wait_for(state="visible", timeout=10000)
        assert new_date_picker.is_visible(), "❌ Date picker is not visible after wait!"

        self.click(new_date_picker)
        print("✅ Date picker opened.")


        self._page.locator(self.NEXT_MONTH_BTN).wait_for(state="visible", timeout=10000)
        assert self._page.locator(self.NEXT_MONTH_BTN).is_visible(), "❌ Next month button not visible"
        self.click(self.NEXT_MONTH_BTN)
        self.click(self.NEXT_MONTH_BTN)
        self.click(self.NEXT_MONTH_BTN)
        self.click(self.NEXT_MONTH_BTN)

        print("✅ Clicked 'next month' 3 times")

        # Alternative flight date route #2

        month_title = self._page.locator(".container__months .month-item:nth-child(1)  .month-item-name")
        month_name_text = self.get_inner_text(month_title)
        print(f"🕓 Current month title: {month_name_text}")

        outbound_flight_2_date = self._fallback_params.get("outbound_flight_2_date")
        outbound_flight_2 = self._page.locator('.container__months .month-item:nth-child(2) .container__days a.day-item').filter(has_text=f"{outbound_flight_2_date}")
        outbound_flight_2.wait_for(state="visible", timeout=10000)
        inbound_flight_2_date = self._fallback_params.get("inbound_flight_2_date")
        inbound_flight_2 = self._page.locator('.container__months .month-item:nth-child(2) .container__days a.day-item').filter(has_text=f"{inbound_flight_2_date}")
        inbound_flight_2.wait_for(state="visible", timeout=10000)

        if outbound_flight_2.is_visible() and inbound_flight_2.is_visible():
            print(f"✅ Dates {outbound_flight_2_date}-{inbound_flight_2_date} are available, selecting them now...")

            # בחירה "קשוחה" עם כל מה שצריך
            outbound_flight_2.scroll_into_view_if_needed()
            outbound_flight_2.hover()
            self.safe_click(outbound_flight_2)
            self._page.wait_for_timeout(300)

            inbound_flight_2.scroll_into_view_if_needed()
            inbound_flight_2.hover()
            self.safe_click(inbound_flight_2)
            self._page.wait_for_timeout(300)

            find_me_flight_btn = self._page.locator(self.FIND_ME_FLIGHTS_BTN)
            find_me_flight_btn.wait_for(state="visible", timeout=10000)
            assert find_me_flight_btn.is_visible(), "❌ Find me flights btn is not visible!"
            self.click(find_me_flight_btn)
            print("✅ Clicked 'Find me flights' button")

            try:
                search_result_element = self._page.locator(self.SEARCH_RESULTS_VERIFY_ELEMENT)
                search_result_element.wait_for(state="visible", timeout=25000)
                print("✅ The search result page was loaded successfully!")

                return True

            except PlaywrightTimeout:

                next_outbound_flight_3_date = self._fallback_params.get("outbound_flight_3_date", "?")
                next_inbound_flight_3_date = self._fallback_params.get("inbound_flight_3_date", "?")
                print(f"❌ Search results not found, trying to select alternative dates {next_outbound_flight_3_date}-{next_inbound_flight_3_date}")
                return self.alternative_flight_dates_3()

        next_outbound_flight_3_date = self._fallback_params.get("outbound_flight_3_date", "?")
        next_inbound_flight_3_date = self._fallback_params.get("inbound_flight_3_date", "?")
        print(f"❌ The flight route ({outbound_flight_2_date}–{inbound_flight_2_date}) is not available, Trying alternative dates: {next_outbound_flight_3_date}-{next_inbound_flight_3_date}")

        return self.alternative_flight_dates_3()

    def alternative_flight_dates_3(self,):

        new_search_result_element = self._page.locator(self.NEW_SEARCH_RESULT_PAGE_ELEMENT)
        new_search_result_element.wait_for(state="visible", timeout=10000)
        assert new_search_result_element.is_visible(), "❌ The new search result element is not visible!"
        self.click(new_search_result_element)
        print("✅ The new search result element is visible!")

        new_date_picker = self._page.locator(self.DATE_PICKER)
        new_date_picker.wait_for(state="visible", timeout=10000)
        assert new_date_picker.is_visible(), "❌ The new date picker is not visible!"
        self.click(new_date_picker)
        print("✅ Date picker opened.")

        next_month_btn = self._page.locator(self.NEXT_MONTH_BTN)
        next_month_btn.wait_for(state="visible", timeout=10000)
        assert next_month_btn.is_visible(), "❌, The next month btn is not visible!"
        self.click(self.DATE_PICKER)
        print("✅ Date picker opened")

        self._page.locator(self.NEXT_MONTH_BTN).wait_for(state="visible", timeout=10000)
        assert self._page.locator(self.NEXT_MONTH_BTN).is_visible(), "❌ Next month button not visible"
        self.click(self.NEXT_MONTH_BTN)
        self.click(self.NEXT_MONTH_BTN)
        self.click(self.NEXT_MONTH_BTN)

        print("✅ Clicked 'next month' three times")

        month_title = self._page.locator(".container__months .month-item:nth-child(2)  .month-item-name")
        month_name_text = self.get_inner_text(month_title)
        print(f"🕓 Current month title: {month_name_text}")

        outbound_flight_3_date = self._fallback_params.get("outbound_flight_3_date")
        outbound_flight_3 = self._page.locator('.container__months .month-item:nth-child(1) .container__days a.day-item').filter(has_text=f"{outbound_flight_3_date}")
        outbound_flight_3.wait_for(state="visible", timeout=10000)

        inbound_flight_3_date= self._fallback_params.get("inbound_flight_3_date")
        inbound_flight_3 = self._page.locator('.container__months .month-item:nth-child(1) .container__days a.day-item').filter(has_text=f"{inbound_flight_3_date}")
        inbound_flight_3.wait_for(state="visible", timeout=10000)

        if outbound_flight_3.is_visible() and inbound_flight_3.is_visible():
            print("✅ Dates 14–21 are available (option 3), selecting them now...")
            self.click(outbound_flight_3)
            self.click(inbound_flight_3)

            find_me_flight_btn = self._page.locator(self.FIND_ME_FLIGHTS_BTN)
            find_me_flight_btn.wait_for(state="visible", timeout=10000)
            assert find_me_flight_btn.is_visible(), "❌ Find me flights btn is not visible!"
            self.click(find_me_flight_btn)
            print("✅ Clicked 'Find me flights' button")


            try:
                search_result_element = self._page.locator(self.SEARCH_RESULTS_VERIFY_ELEMENT)
                search_result_element.wait_for(state="visible", timeout=25000)
                print("✅ The search result page was loaded successfully!")

                return True

            except PlaywrightTimeout:

                next_outbound_flight_4_date = self._fallback_params.get("outbound_flight_4_date", "?")
                next_inbound_flight_4_date = self._fallback_params.get("inbound_flight_4_date", "?")

                print(f"❌ Search results not found, trying to select alternative dates and destination {next_outbound_flight_4_date}-{next_inbound_flight_4_date}")

                return self.alternative_flight_destination_and_dates_1()

        next_outbound_flight_4_date = self._fallback_params.get("outbound_flight_4_date", "?")
        next_inbound_flight_4_date = self._fallback_params.get("inbound_flight_4_date", "?")

        print(f"❌ The alternative flight dates {outbound_flight_3_date}-{inbound_flight_3_date} are not available, choosing different destination and dates {next_outbound_flight_4_date}-{next_inbound_flight_4_date}...")
        return self.alternative_flight_destination_and_dates_1()

    def alternative_flight_destination_and_dates_1(self):

        # Choose alternative destination and date #1

        print("✅ Starting fallback for destination and date #1")

        new_search_result_element = self._page.locator(self.NEW_SEARCH_RESULT_PAGE_ELEMENT)
        new_search_result_element.wait_for(state="visible", timeout=10000)
        assert new_search_result_element.is_visible(), "❌ The new search result element is not visible!"
        self.click(new_search_result_element)
        print("✅ The new search result element is visible!")

        print("Selecting outbound flight")
        choose_outbound_flight_btn = self._page.locator(self.CHOOSE_OUTBOUND_FLIGHT_BTN)
        choose_outbound_flight_btn.wait_for(state="visible", timeout=10000)
        assert choose_outbound_flight_btn.is_visible(), "❌ The outbound flight btn is not visible!"
        self.click(choose_outbound_flight_btn)
        print("✅ Outbound flight button clicked")

        outbound_city = self._fallback_params.get("outbound_city_fallback_param")
        print(f"ℹ️ Typing outbound city: {outbound_city}")
        outbound_field = self._page.locator(self.OUTBOUND_FLIGHT_CITY_TITLE)
        outbound_field.click()
        outbound_field.press("Control+A")
        outbound_field.press("Backspace")
        outbound_field.fill(outbound_city)

        suggestion = self._page.locator(self.ACTUAL_OUTBOUND_CITY)
        suggestion.wait_for(state="visible", timeout=10000)

        assert outbound_city in suggestion.inner_text(), f"❌ '{outbound_city}' not found in suggestions!"
        self.click(suggestion)
        print("✅ Outbound city selected.")


        print("Selecting inbound flight")
        choose_inbound_flight_btn = self._page.locator(self.CHOOSE_INBOUND_FLIGHT_BTN)
        choose_inbound_flight_btn.wait_for(state="visible", timeout=10000)
        assert choose_inbound_flight_btn.is_visible(), "❌ The inbound flight btn is not visible!"
        self.click(choose_inbound_flight_btn)
        print("✅ The inbound flight btn was clicked successfully!")

        inbound_city = self._fallback_params.get("inbound_city_fallback_param")
        print(f"ℹ️ Typing inbound city: {inbound_city}")
        inbound_field = self._page.locator(self.INBOUND_FLIGHT_CITY_TITLE)
        self.click(inbound_field)
        inbound_field.press("Control+A")
        inbound_field.press("Backspace")
        inbound_field.fill(inbound_city)
        self._page.wait_for_timeout(1000)
        self.click(self.ACTUAL_INBOUND_CITY)
        print("✅ Inbound city selected.")

        # מוודאים שבורר התאריכים נפתח
        new_date_picker = self._page.locator(self.DATE_PICKER)
        new_date_picker.wait_for(state="visible", timeout=10000)
        assert new_date_picker.is_visible(), "❌ The new date picker is not visible!"
        self.click(new_date_picker)
        print("✅ Date picker opened.")

        next_month_btn = self._page.locator(self.NEXT_MONTH_BTN)
        next_month_btn.wait_for(state="visible", timeout=10000)
        assert next_month_btn.is_visible(), "❌ The next month btn is not visible!"
        self.click(next_month_btn)
        self.click(self.NEXT_MONTH_BTN)
        self.click(self.NEXT_MONTH_BTN)
        print("✅ The next month button clicked.")

        month_title = self._page.locator(".container__months .month-item:nth-child(2)  .month-item-name")
        month_name_text = self.get_inner_text(month_title)
        print(f"🕓 Current month title: {month_name_text}")

        outbound_flight_4_date = self._fallback_params.get("outbound_flight_4_date")
        outbound_flight_4 = self._page.locator('.container__months .month-item:nth-child(2) .container__days a.day-item').filter(has_text=f"{outbound_flight_4_date}")
        outbound_flight_4.wait_for(state="visible", timeout=10000)

        inbound_flight_4_date = self._fallback_params.get("inbound_flight_4_date")
        inbound_flight_4 = self._page.locator('.container__months .month-item:nth-child(2) .container__days a.day-item').filter(has_text=f"{inbound_flight_4_date}")
        inbound_flight_4.wait_for(state="visible", timeout=10000)

        #Alternative flight destination and date route #4

        if outbound_flight_4.is_visible() and inbound_flight_4.is_visible():
            print(f"✅ The alternative dates ({outbound_flight_4_date}–{inbound_flight_4_date}) are visible!")
            self.click(outbound_flight_4)
            self.click(inbound_flight_4)
            print("✅ (option 4) Dates selected successfully.")

            find_me_flight_btn = self._page.locator(self.FIND_ME_FLIGHTS_BTN)
            find_me_flight_btn.wait_for(state="visible", timeout=10000)
            assert find_me_flight_btn.is_visible(), "❌ Find me flights btn is not visible!"
            self.click(find_me_flight_btn)
            print("✅ Find me flights button clicked.")


            try:
                search_result_element = self._page.locator(self.SEARCH_RESULTS_VERIFY_ELEMENT)
                search_result_element.wait_for(state="visible", timeout=25000)
                print("✅ The search result page was loaded successfully!")

                return True

            except PlaywrightTimeout:

                next_outbound_flight_5 = self._fallback_params.get("outbound_flight_5_date", "?")
                next_inbound_flight_5 = self._fallback_params.get("outbound_flight_5_date", "?")

                print(f"❌ Search results not found, trying to select alternative dates {next_outbound_flight_5}-{next_inbound_flight_5}")

                return self.alternative_flight_destination_and_dates_2()

        next_outbound_flight_5 = self._fallback_params.get("outbound_flight_5_date", "?")
        next_inbound_flight_5 = self._fallback_params.get("outbound_flight_5_date", "?")

        print(f"❌ The alternative flight dates {outbound_flight_4_date}-{inbound_flight_4_date} are not available, choosing different date {next_outbound_flight_5}-{next_inbound_flight_5}...")
        return self.alternative_flight_destination_and_dates_2()



    def alternative_flight_destination_and_dates_2(self):

        # Choose alternative destination and date #2

        print("✅ Starting fallback for destination and date #1")

        new_search_result_element = self._page.locator(self.NEW_SEARCH_RESULT_PAGE_ELEMENT)
        new_search_result_element.wait_for(state="visible", timeout=10000)
        assert new_search_result_element.is_visible(), "❌ The new search result element is not visible!"
        self.click(new_search_result_element)
        print("✅ The new search result element is visible!")

        print("Selecting outbound flight")
        choose_outbound_flight_btn = self._page.locator(self.CHOOSE_OUTBOUND_FLIGHT_BTN)
        choose_outbound_flight_btn.wait_for(state="visible", timeout=10000)
        assert choose_outbound_flight_btn.is_visible(), "❌ The outbound flight btn is not visible!"
        self.click(choose_outbound_flight_btn)
        print("✅ Outbound flight button clicked.")

        outbound_city = self._fallback_params.get("outbound_city_fallback_param")
        print(f"ℹ️ Typing outbound city: {outbound_city}")
        outbound_field = self._page.locator(self.OUTBOUND_FLIGHT_CITY_TITLE)
        outbound_field.click()
        outbound_field.press("Control+A")
        outbound_field.press("Backspace")
        outbound_field.fill(outbound_city)

        suggestion = self._page.locator(self.ACTUAL_OUTBOUND_CITY)
        suggestion.wait_for(state="visible", timeout=10000)
        assert outbound_city in suggestion.inner_text(), f"❌ '{outbound_city}' not found in suggestions!"
        self.click(suggestion)
        print("✅ Outbound city selected.")

        print("Selecting inbound flight")
        inbound_city = self._fallback_params.get("inbound_city_fallback_param")
        choose_inbound_flight_btn = self._page.locator(self.CHOOSE_INBOUND_FLIGHT_BTN)
        choose_inbound_flight_btn.wait_for(state="visible", timeout=10000)
        assert choose_inbound_flight_btn.is_visible(), "❌ The inbound flight btn is not visible!"
        self.click(choose_inbound_flight_btn)
        print("✅ Inbound flight button clicked.")

        print(f"ℹ️ Typing inbound city: {inbound_city}")
        inbound_field = self._page.locator(self.INBOUND_FLIGHT_CITY_TITLE)
        inbound_field.click()
        inbound_field.press("Control+A")
        inbound_field.press("Backspace")
        inbound_field.fill(inbound_city)
        self._page.wait_for_timeout(1000)
        self.click(self.ACTUAL_INBOUND_CITY)
        print("✅ Inbound city selected.")

        # פתיחת בורר התאריכים
        new_date_picker = self._page.locator(self.DATE_PICKER)
        new_date_picker.wait_for(state="visible", timeout=10000)
        assert new_date_picker.is_visible(), "❌ The new date picker is not visible!"
        self.click(new_date_picker)
        print("✅ Date picker opened.")

        next_month_btn = self._page.locator(self.NEXT_MONTH_BTN)
        next_month_btn.wait_for(state="visible", timeout=10000)
        assert next_month_btn.is_visible(), "❌ The next month button is not visible!"
        self.click(next_month_btn)
        self.click(self.NEXT_MONTH_BTN)
        print("✅ The next month button clicked.")

        month_title = self._page.locator(".container__months .month-item:nth-child(1)  .month-item-name")
        month_name_text = self.get_inner_text(month_title)
        print(f"🕓 Current month title: {month_name_text}")

        outbound_flight_5_date = self._fallback_params.get("outbound_flight_5_date")
        outbound_flight_5 = self._page.locator('.container__months .month-item:nth-child(2) .container__days a.day-item').filter(has_text=f"{outbound_flight_5_date}")
        outbound_flight_5.wait_for(state="visible", timeout=10000)

        inbound_flight_5_date = self._fallback_params.get("inbound_flight_5_date")
        inbound_flight_5 = self._page.locator('.container__months .month-item:nth-child(2) .container__days a.day-item').filter(has_text=f"{inbound_flight_5_date}")
        inbound_flight_5.wait_for(state="visible", timeout=10000)

        if outbound_flight_5.is_visible() and inbound_flight_5.is_visible():
            print(f"✅ The alternative dates ({outbound_flight_5_date}–{inbound_flight_5_date}) are visible!")
            self.click(outbound_flight_5)
            self.click(inbound_flight_5)
            print("✅ Dates selected successfully.")

            find_me_flight_btn = self._page.locator(self.FIND_ME_FLIGHTS_BTN)
            find_me_flight_btn.wait_for(state="visible", timeout=10000)
            assert find_me_flight_btn.is_visible(), "❌ Find me flights button is not visible!"
            self.click(find_me_flight_btn)
            print("✅ Find me flights button clicked.")

            try:
                search_result_element = self._page.locator(self.SEARCH_RESULTS_VERIFY_ELEMENT)
                search_result_element.wait_for(state="visible", timeout=25000)
                print("✅ The search result page was loaded successfully!")

                return True

            except PlaywrightTimeout:
                    print("❌ Search results not found!")

        print(f"❌ The alternative flight dates {outbound_flight_5_date}-{inbound_flight_5_date} are not available! There are no available flight!")
        raise AssertionError("❌ No available flight options found after all fallback attempts!")

    def check_el_al_airways_airline_filter(self):

        show_more_airlines_btn =  self._page.locator(self.SHOW_MORE_AIRLINES_BTN)
        show_more_airlines_btn.wait_for(state="visible", timeout=10000)
        assert show_more_airlines_btn.is_visible(), "❌ Show more airlines btn is not visible!"
        self.click(show_more_airlines_btn)
        print("✅ Show more airlines btn was clicked!")

        el_al_airways_checkbox = self._page.locator(self.ELAL_FILTER_CHECK)
        assert el_al_airways_checkbox.is_visible(), "❌ el_al_airways_airlines filter checkbox is not visible on the page!"

        self.click(el_al_airways_checkbox)
        print("✅ el_al_airways_airlines filter checkbox was clicked successfully.")

    def click_more_flight_button_up_to_six_times(self):
        show_more_flight_btn = self._page.locator(self.SHOW_MORE_FLIGHTS_BTN)

        for i in range(6):
            if show_more_flight_btn.count() == 0 or not show_more_flight_btn.is_visible():
                print(f"ℹ️ 'More flights' button not found or no longer visible – stopping at attempt {i}.")
                break
            try:
                show_more_flight_btn.click(force=True)
                print(f"✅ Clicked 'More flights' button ({i + 1}/6)")
                self._page.wait_for_timeout(1000)  # זמן טעינה אחרי לחיצה
            except Exception as e:
                print(f"⚠️ Failed to click on attempt {i + 1}: {e}")
                break

    def choose_el_al_airways_flight(self):
        if not hasattr(self, "tried_fallbacks"):
            self.tried_fallbacks = set()

        self._page.wait_for_timeout(5000)
        print("🌐 Current URL:", self._page.url)
        print("✈️ Choosing el_al_airways flight...")


        flight_cards_list = self._page.locator(self.FLIGHT_CARD_LIST)
        flight_cards_list.wait_for(state="visible", timeout=10000)
        assert flight_cards_list.is_visible(), "❌ Flight search results are not visible!"
        print("✅ Flight search results are visible.")

        available_flights_segments = self._page.locator(self.AVAILABLE_FLIGHTS_SEGMENTS)
        count = available_flights_segments.count()
        for i in range(count):
            segment = available_flights_segments.nth(i)

            elal_outbound_flight_text = segment.locator(self.SEGMENT_OUTBOUND_FLIGHT_TEXT).first
            elal_outbound_flight_text.wait_for(state="visible", timeout=10000)
            outbound_airline_name = elal_outbound_flight_text.inner_text().strip().lower()

            elal_inbound_flight_text = segment.locator(self.SEGMENT_INBOUND_FLIGHT_TEXT).first
            elal_inbound_flight_text.wait_for(state="visible", timeout=10000)
            inbound_airline_name = elal_inbound_flight_text.inner_text().strip().lower()

            if "el al" in outbound_airline_name:
                print("✅ el_al_airways outbound flight found.")
            else:
                print(f"❌ el_al_airways outbound flight not found in flight #{i + 1}")

            if "abcd" in inbound_airline_name:
                print("✅ el_al_airways inbound flight found.")
            else:
                print(f"❌ el_al_airways inbound flight not found in flight #{i + 1}")

            if "el al" in outbound_airline_name and "abcd" in inbound_airline_name:
                self.saved_flight_data.outbound_departure_time = segment.locator(
                    self.FLIGHT_OUTBOUND_DEPARTURE_TIME).inner_text()
                print("Outbound departure time:", self.saved_flight_data.outbound_departure_time)

                self.saved_flight_data.outbound_departure_date = segment.locator(
                    self.FLIGHT_OUTBOUND_DEPARTURE_DATE).inner_text().replace('\n', ' ').strip()
                print("Outbound departure date:", self.saved_flight_data.outbound_departure_date)

                self.saved_flight_data.outbound_departure_iata_origin = segment.locator(
                    self.FLIGHT_OUTBOUND_DEPARTURE_IATA_ORIGIN).inner_text()
                print("Flight outbound departure origin IATA:", self.saved_flight_data.outbound_departure_iata_origin)

                self.saved_flight_data.outbound_landing_time = segment.locator(
                    self.FLIGHT_OUTBOUND_LANDING_TIME).inner_text()
                print("Outbound landing time:", self.saved_flight_data.outbound_landing_time)

                self.saved_flight_data.outbound_landing_date = segment.locator(
                    self.FLIGHT_OUTBOUND_LANDING_DATE).inner_text().replace('\n', ' ').strip()
                print("Outbound landing date:", self.saved_flight_data.outbound_landing_date)

                self.saved_flight_data.outbound_landing_iata_destination = segment.locator(
                    self.FLIGHT_OUTBOUND_LANDING_IATA_DESTINATION).inner_text()
                print("Flight outbound landing IATA destination:",
                      self.saved_flight_data.outbound_landing_iata_destination)

                self.saved_flight_data.inbound_departure_time = segment.locator(
                    self.FLIGHT_INBOUND_DEPARTURE_TIME).inner_text()
                print("Inbound departure time:", self.saved_flight_data.inbound_departure_time)

                self.saved_flight_data.inbound_departure_date = segment.locator(
                    self.FLIGHT_INBOUND_DEPARTURE_DATE).inner_text().replace('\n', ' ').strip()
                print("Inbound departure date:", self.saved_flight_data.inbound_departure_date)

                self.saved_flight_data.inbound_departure_iata_origin = segment.locator(
                    self.FLIGHT_INBOUND_DEPARTURE_IATA_ORIGIN).inner_text()
                print("Flight inbound departure origin IATA:", self.saved_flight_data.inbound_departure_iata_origin)

                self.saved_flight_data.inbound_landing_time = segment.locator(
                    self.FLIGHT_INBOUND_LANDING_TIME).inner_text()
                print("Inbound landing time:", self.saved_flight_data.inbound_landing_time)

                self.saved_flight_data.inbound_landing_date = segment.locator(
                    self.FLIGHT_INBOUND_LANDING_DATE).inner_text().replace('\n', ' ').strip()
                print("Inbound landing date:", self.saved_flight_data.inbound_landing_date)

                self.saved_flight_data.inbound_landing_iata_destination = segment.locator(
                    self.FLIGHT_INBOUND_LANDING_IATA_DESTINATION).inner_text()
                print("Flight inbound landing IATA destination:",
                      self.saved_flight_data.inbound_landing_iata_destination)

                self.saved_flight_data.outbound_duration_time = segment.locator(
                    self.FLIGHT_OUTBOUND_DURATION).inner_text().replace('\n', ' ').strip()
                print("Flight outbound duration time:", self.saved_flight_data.outbound_duration_time)

                self.saved_flight_data.inbound_duration_time = segment.locator(
                    self.FLIGHT_INBOUND_DURATION).inner_text().replace('\n', ' ').strip()
                print("Flight inbound duration time:", self.saved_flight_data.inbound_duration_time)

                order_flight_btn = segment.locator(self.ORDER_FLIGHT_BTN)
                order_flight_btn.wait_for(state="attached", timeout=10000)
                print("🟢 el_al_airways_airlines round trip found! Booking now...")


                with self._page.context.expect_page() as flexi_page_info:
                    self.click(order_flight_btn)

                flexi_page = flexi_page_info.value
                flexi_page.wait_for_load_state()
                return flexi_page

        print("🔁 No el_al_airways flight found — trying alternative dates (1)...")
        if "dates1" not in self.tried_fallbacks and self.alternative_flight_dates_1():
            self.tried_fallbacks.add("dates1")
            self.check_el_al_airways_airline_filter()
            self.click_more_flight_button_up_to_six_times()
            return self.choose_el_al_airways_flight()

        print("🔁 Trying alternative dates (2)...")
        if "dates2" not in self.tried_fallbacks and self.alternative_flight_dates_2():
            self.tried_fallbacks.add("dates2")
            self.check_el_al_airways_airline_filter()
            self.click_more_flight_button_up_to_six_times()
            return self.choose_el_al_airways_flight()

        print("🔁 Trying alternative dates (3)...")
        if "dates3" not in self.tried_fallbacks and self.alternative_flight_dates_3():
            self.tried_fallbacks.add("dates3")
            self.check_el_al_airways_airline_filter()
            self.click_more_flight_button_up_to_six_times()
            return self.choose_el_al_airways_flight()

        print("🔁 Trying alternative destination and dates (4)...")
        if "dest1" not in self.tried_fallbacks and self.alternative_flight_destination_and_dates_1():
            self.tried_fallbacks.add("dest1")
            self.check_el_al_airways_airline_filter()
            self.click_more_flight_button_up_to_six_times()
            return self.choose_el_al_airways_flight()

        print("🔁 Trying alternative destination and dates (5)...")
        if "dest2" not in self.tried_fallbacks and self.alternative_flight_destination_and_dates_2():
            self.tried_fallbacks.add("dest2")
            self.check_el_al_airways_airline_filter()
            self.click_more_flight_button_up_to_six_times()
            return self.choose_el_al_airways_flight()

        raise AssertionError("❌ No round trip el_al_airways_airlines flight was found in the available search results.")


