from playwright.sync_api import Page, Locator
from lastminute_co_il_flights_automation.pages.base_page import BasePage
from lastminute_co_il_flights_automation.pages.page3_flexi_page import TrolleyStatus, BaggageStatus
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class ContactPage(BasePage):
    def __init__(self,
                 page: Page,
                 outbound_baggage_status: str,
                 inbound_baggage_status: str,
                 outbound_trolley_status: str,
                 inbound_trolley_status: str
    ):
        super().__init__(page)
        self.outbound_baggage_status = outbound_baggage_status
        self.inbound_baggage_status = inbound_baggage_status
        self.outbound_trolley_status = outbound_trolley_status
        self.inbound_trolley_status = inbound_trolley_status

    CONTACT_HEADER = '.header-desktop > [key="Checkout.ContactDetails"]'
    CONTACT_FIRST_NAME_FIELD = '[name="fname"]'
    CONTACT_LAST_NAME_FIELD = '[name="lname"]'
    CONTACT_EMAIL_ADDRESS_FIELD = '[name="email"]'
    CONTACT_EMAIL_ADDRESS_CONFIRMATION_FIELD = '[name="emailConfirm"]'
    CONTACT_PHONE_NUMBER_DROPDOWN = ".dropdown-subject.show"
    CONTACT_PHONE_NUMBER_FIELD = '[name="phone"]'
    CONTACT_PROMOTION_BTN = "#allowSubscribe"
    CONTACT_CONTINUE_BTN = ".continue-wrapper .continue"
    PASSENGER_FIRST_NAME_FIELD = '[name="paxFName"]'
    PASSENGER_LAST_NAME_FIELD = '[name="paxLName"]'
    PASSENGER_BIRTHDAY_DATE = '[name="paxBirthDate"]'
    PASSENGER_GENDER_DROPDOWN = ".subject-wrapper .dropdown-subject.gender-dropdown"
    PASSENGER_DROPDOWN_SELECT_MALE_GENDER = ".options-container.gender-dropdown-options.show > .option:nth-child(1)"
    PASSENGER_PASSPORT_NUMBER_FIELD = '[placeholder="מספר דרכון"]'
    PASSENGER_PASSPORT_EXPIRATION_DATE_FIELD = 'app-input:nth-child(6) [placeholder="dd/mm/yyyy"]'
    PASSENGER_NATIONALITY_DROPDOWN = '.inputs-wrapper .selector-input-wrapper:nth-of-type(2) .subject-wrapper > [class^="dropdown-subject"]'
    COUNTRY_OF_PASSPORT_ISSUANCE_DROPDOWN = '.inputs-wrapper .selector-input-wrapper:nth-of-type(3) .subject-wrapper [class^="dropdown-subject"]'
    CHOOSE_NATIONALITY_ISRAEL = ".inputs-wrapper .selector-input-wrapper:nth-of-type(2) .subject-wrapper > .options-container > .option:nth-child(1)"
    CHOOSE_ISSUE_COUNTRY_ISRAEL = ".inputs-wrapper .selector-input-wrapper:nth-of-type(3) .subject-wrapper .option:nth-child(1)"
    DO_NOT_ADD_BAGGAGE_OUTBOUND = ".baggages-wrapper .baggage-segment:nth-child(1) .baggage-upgrade-row:nth-child(3) .baggage-item:nth-child(1)"
    DO_NOT_ADD_BAGGAGE_INBOUND = ".baggages-wrapper .baggage-segment:nth-child(2) .baggage-upgrade-row:nth-child(3) .baggage-item:nth-child(1)"
    ADD_ONE_BAGGAGE_OUTBOUND = ".baggages-wrapper .baggage-segment:nth-child(1) .baggage-item:nth-child(2)"
    ADD_ONE_BAGGAGE_INBOUND = '.baggages-wrapper .baggage-segment:nth-child(2) .baggage-item:nth-child(2):has-text("מזוודה")'
    PASSENGER_CONTINUE_BTN = ".continue-btn-wrapper > .continue-btn"
    ADD_ONE_TROLLEY_OUTBOUND = ".baggages-wrapper .baggage-segment:nth-child(1) .baggage-upgrade-row:nth-child(2) .baggage-item:nth-child(2)"
    ADD_ONE_TROLLEY_INBOUND = ".baggages-wrapper .baggage-segment:nth-child(2) .baggage-upgrade-row:nth-child(2) .baggage-item:nth-child(2)"
    ASSERT_INCLUDED_OUTBOUND_BAGGAGE = ".baggages-wrapper .baggage-segment:nth-child(1) .baggage-upgrade-row:nth-child(3) .baggage-item.free-of-charge-baggage"
    ASSERT_INCLUDED_INBOUND_BAGGAGE = ".baggages-wrapper .baggage-segment:nth-child(2) .baggage-upgrade-row:nth-child(3) .baggage-item.free-of-charge-baggage"
    ASSERT_INCLUDED_OUTBOUND_TROLLEY = ".baggages-wrapper .baggage-segment:nth-child(1) .baggage-upgrade-row:nth-child(2) .baggage-item.free-of-charge-baggage"
    ASSERT_INCLUDED_INBOUND_TROLLEY = ".baggages-wrapper .baggage-segment:nth-child(2) .baggage-upgrade-row:nth-child(2) .baggage-item.free-of-charge-baggage"

    def wait_for_contact_page_to_load(self):
        print("📨 Navigating to contact details page...")
        self._page.wait_for_load_state("load")

        contact_header = self._page.locator(self.CONTACT_HEADER)
        contact_header.wait_for(state="visible", timeout=10000)

        assert contact_header.is_visible(), "❌ Contact details page did not load!"
        print("✅ Contact details page loaded successfully.")

    def fill_contact_info(self, first_name, last_name, email, verify_email, phone_number):
        self._page.wait_for_timeout(1000)

        first_name_field = self._page.locator(self.CONTACT_FIRST_NAME_FIELD)
        first_name_field.wait_for(state="visible", timeout=10000)
        assert first_name_field.is_visible(), "❌ First name field is not visible!"
        self.fill_info(first_name_field, first_name)
        print("✅ First name filled.")

        last_name_field = self._page.locator(self.CONTACT_LAST_NAME_FIELD)
        assert last_name_field.is_visible(), "❌ Last name field is not visible!"
        self.fill_info(last_name_field, last_name)
        print("✅ Last name filled.")

        email_field = self._page.locator(self.CONTACT_EMAIL_ADDRESS_FIELD)
        assert email_field.is_visible(), "❌ Email field is not visible!"
        self.fill_info(email_field, email)
        print("✅ Email filled.")

        confirm_email_field = self._page.locator(self.CONTACT_EMAIL_ADDRESS_CONFIRMATION_FIELD)
        assert confirm_email_field.is_visible(), "❌ Email confirmation field is not visible!"
        self.fill_info(confirm_email_field, verify_email)
        print("✅ Email confirmation filled.")

        phone_field = self._page.locator(self.CONTACT_PHONE_NUMBER_FIELD)
        assert phone_field.is_visible(), "❌ Phone number field is not visible!"
        self.fill_info(phone_field, phone_number)
        print("✅ Phone number filled.")

        promotion_checkbox = self._page.locator(self.CONTACT_PROMOTION_BTN)
        assert promotion_checkbox.is_visible(), "❌ Promotions checkbox not found!"
        if not promotion_checkbox.is_checked():
            self.click(promotion_checkbox)
            print("✅ Promotions checkbox selected.")
        else:
            print("ℹ️ Promotions checkbox already selected.")

        continue_btn = self._page.locator(self.CONTACT_CONTINUE_BTN)
        continue_btn.wait_for(state="visible", timeout=10000)
        assert continue_btn.is_visible(), "❌ 'Continue' button is not visible!"
        self.click(continue_btn)
        self._page.wait_for_timeout(5000)
        print("➡️ Proceeding to passenger details page.")

    def fill_passenger_info(self, passenger_first_name, passenger_last_name, birthday_date):
        self._page.wait_for_timeout(5000)
        print("✍️ Filling passenger information...")

        # Fill first name
        first_name_field = self._page.locator(self.PASSENGER_FIRST_NAME_FIELD)
        first_name_field.wait_for(state="visible", timeout=10000)
        assert first_name_field.is_visible(), "❌ Passenger first name field is not visible!"
        self.fill_info(first_name_field, passenger_first_name)
        print("✅ Passenger first name filled.")

        # Fill last name
        last_name_field = self._page.locator(self.PASSENGER_LAST_NAME_FIELD)
        assert last_name_field.is_visible(), "❌ Passenger last name field is not visible!"
        self.fill_info(last_name_field, passenger_last_name)
        print("✅ Passenger last name filled.")

        # Fill birthday
        birthday_field = self._page.locator(self.PASSENGER_BIRTHDAY_DATE)
        assert birthday_field.is_visible(), "❌ Passenger birthday field is not visible!"
        self.fill_info(birthday_field, birthday_date)
        print("✅ Passenger birthday filled.")

        # Open gender dropdown and select male gender
        gender_dropdown = self._page.locator(self.PASSENGER_GENDER_DROPDOWN)
        gender_dropdown.wait_for(state="visible", timeout=15000)
        assert gender_dropdown.is_visible(), "❌ Passenger gender dropdown is not visible!"
        self.click(gender_dropdown)
        print("✅ Gender dropdown clicked.")

        male_gender = self._page.locator(self.PASSENGER_DROPDOWN_SELECT_MALE_GENDER)
        assert male_gender.is_visible, "❌ Male gender is not visible!"
        self.click(male_gender)
        print("✅ Male gender was selected!")

    def fill_passport_and_nationality_fields(self, passport_number, passport_expiration_date):
        #Fill passenger passport number
        passport_field = self._page.locator(self.PASSENGER_PASSPORT_NUMBER_FIELD)
        if passport_field.count() > 0 and passport_field.is_visible():
            self.fill_info(passport_field, passport_number)
            print("✅ Passenger passport number filled.")
        else:
            print("ℹ️ Passenger passport number field not found – skipping.")

        #Fill passport_expiration_date
        passport_expiration_field = self._page.locator(self.PASSENGER_PASSPORT_EXPIRATION_DATE_FIELD)
        if passport_expiration_field.count() > 0 and passport_expiration_field.is_visible():
            self.fill_info(passport_expiration_field, passport_expiration_date)
            print("✅ Passenger passport expiration date filled.")
        else:
            print("ℹ️ Passport expiration field not found – skipping.")

        # Open passenger nationality dropdown and select Israel
        passenger_nationality_dropdown = self._page.locator(self.PASSENGER_NATIONALITY_DROPDOWN)
        if passenger_nationality_dropdown.count() > 0 and passenger_nationality_dropdown.is_visible():
            self.click(passenger_nationality_dropdown)
            print("🔽 Passenger nationality dropdown clicked.")

            israel_option = self._page.locator(self.CHOOSE_NATIONALITY_ISRAEL)
            if israel_option.count() > 0 and israel_option.is_visible():
                self.click(israel_option)
                print("✅ Israel nationality selected.")
            else:
                print("ℹ️ Nationality option for Israel not found – skipping.")
        else:
            print("ℹ️ Nationality dropdown not found – skipping.")

        # Open passenger passport issuing country dropdown and select Israel
        country_of_issuance_dropdown = self._page.locator(self.COUNTRY_OF_PASSPORT_ISSUANCE_DROPDOWN)
        if country_of_issuance_dropdown.count() > 0 and country_of_issuance_dropdown.is_visible():
            self.click(country_of_issuance_dropdown)
            print("🔽 Passport issuing country dropdown clicked.")

            choose_issue_country_israel = self._page.locator(self.CHOOSE_ISSUE_COUNTRY_ISRAEL)
            if choose_issue_country_israel.count() > 0 and choose_issue_country_israel.is_visible():
                self.click(choose_issue_country_israel)
                print("✅ Passport issuing country 'Israel' selected.")
            else:
                print("ℹ️ 'Israel' option in issuing country not found – skipping.")
        else:
            print("ℹ️ Passport issuing country dropdown not found – skipping.")

    def handle_luggage(self):
        # Outbound Baggage
        if self.outbound_baggage_status == BaggageStatus.ADDABLE.value:
            self.add_outbound_baggage()
        elif self.outbound_baggage_status == BaggageStatus.INCLUDED.value:
            self.assert_included_outbound_baggage()
        elif self.outbound_baggage_status == BaggageStatus.NOT_INCLUDED.value:
            print("ℹ️ No outbound baggage included or available – skipping.")
        else:
            print(f"⚠️ Unknown outbound baggage status: {self.outbound_baggage_status}")

        # Inbound Baggage
        if self.inbound_baggage_status == BaggageStatus.ADDABLE.value:
            self.add_inbound_baggage()
        elif self.inbound_baggage_status == BaggageStatus.INCLUDED.value:
            self.assert_included_inbound_baggage()
        elif self.inbound_baggage_status == BaggageStatus.NOT_INCLUDED.value:
            print("ℹ️ No inbound baggage included or available – skipping.")
        else:
            print(f"⚠️ Unknown inbound baggage status: {self.inbound_baggage_status}")

        # Outbound Trolley
        if self.outbound_trolley_status == TrolleyStatus.ADDABLE.value:
            self.add_outbound_trolley()
        elif self.outbound_trolley_status == TrolleyStatus.INCLUDED.value:
            self.assert_included_outbound_trolley()
        elif self.outbound_trolley_status == TrolleyStatus.NOT_INCLUDED.value:
            print("ℹ️ No outbound trolley included or available – skipping.")
        else:
            print(f"⚠️ Unknown outbound trolley status: {self.outbound_trolley_status}")

        # Inbound Trolley
        if self.inbound_trolley_status == TrolleyStatus.ADDABLE.value:
            self.add_inbound_trolley()
        elif self.inbound_trolley_status == TrolleyStatus.INCLUDED.value:
            self.assert_included_inbound_trolley()
        elif self.inbound_trolley_status == TrolleyStatus.NOT_INCLUDED.value:
            print("ℹ️ No inbound trolley included or available – skipping.")
        else:
            print(f"⚠️ Unknown inbound trolley status: {self.inbound_trolley_status}")

    def add_outbound_baggage(self):
        outbound_baggage_button = self._page.locator(self.ADD_ONE_BAGGAGE_OUTBOUND)

        if outbound_baggage_button.count() == 0:
            print("⚠️ ADDABLE baggage status received, but button not found – skipping.")
            return

        try:
            outbound_baggage_button.wait_for(state="visible", timeout=5000)
            if outbound_baggage_button.is_visible():
                self.click(outbound_baggage_button)
                print("✅ Outbound baggage was successfully added.")
            else:
                print("⚠️ Baggage button not visible even though it's in the DOM – skipping.")
        except PlaywrightTimeoutError:
            print("⚠️ Timeout waiting for baggage button to appear – skipping.")

    def add_inbound_baggage(self):
        inbound_baggage_button = self._page.locator(self.ADD_ONE_BAGGAGE_INBOUND)

        if inbound_baggage_button.count() == 0:
            print("⚠️ ADDABLE inbound baggage status received, but button not found – skipping.")
            return

        try:
            inbound_baggage_button.wait_for(state="visible", timeout=5000)
            if inbound_baggage_button.is_visible():
                self.click(inbound_baggage_button)
                print("✅ Inbound baggage was successfully added.")
            else:
                print("⚠️ Inbound baggage button in DOM but not visible – skipping.")
        except PlaywrightTimeoutError:
            print("⚠️ Timeout waiting for inbound baggage button – skipping.")

    def add_outbound_trolley(self):
        outbound_trolley_button = self._page.locator(self.ADD_ONE_TROLLEY_OUTBOUND)

        if outbound_trolley_button.count() == 0:
            print("⚠️ ADDABLE outbound trolley status received, but button not found – skipping.")
            return

        try:
            outbound_trolley_button.wait_for(state="visible", timeout=5000)
            if outbound_trolley_button.is_visible():
                self.click(outbound_trolley_button)
                print("✅ Outbound trolley was successfully added.")
            else:
                print("⚠️ Outbound trolley button in DOM but not visible – skipping.")
        except PlaywrightTimeoutError:
            print("⚠️ Timeout waiting for outbound trolley button – skipping.")

    def add_inbound_trolley(self):
        inbound_trolley_button = self._page.locator(self.ADD_ONE_TROLLEY_INBOUND)

        if inbound_trolley_button.count() == 0:
            print("⚠️ ADDABLE inbound trolley status received, but button not found – skipping.")
            return

        try:
            inbound_trolley_button.wait_for(state="visible", timeout=5000)
            if inbound_trolley_button.is_visible():
                self.click(inbound_trolley_button)
                print("✅ Inbound trolley was successfully added.")
            else:
                print("⚠️ Inbound trolley button in DOM but not visible – skipping.")
        except PlaywrightTimeoutError:
            print("⚠️ Timeout waiting for inbound trolley button – skipping.")

    def assert_included_outbound_baggage(self):
        included_outbound_baggage = self._page.locator(self.ASSERT_INCLUDED_OUTBOUND_BAGGAGE)
        if included_outbound_baggage.count() == 0:
            raise Exception("❌ Outbound included baggage button not found in DOM at all.")
        included_outbound_baggage.wait_for(state="visible", timeout=20000)
        assert included_outbound_baggage.is_visible(), "❌ Outbound baggage button is not visible!"
        print("✅ Outbound baggage is included.")

    def assert_included_inbound_baggage(self):
        included_inbound_baggage = self._page.locator(self.ASSERT_INCLUDED_INBOUND_BAGGAGE)
        if included_inbound_baggage.count() == 0:
            raise Exception("❌ Inbound included baggage button not found in DOM at all.")
        included_inbound_baggage.wait_for(state="visible", timeout=20000)
        assert included_inbound_baggage.is_visible(), "❌ Inbound baggage button is not visible!"
        print("✅ Inbound baggage is included.")

    def assert_included_outbound_trolley(self):
        included_outbound_trolley = self._page.locator(self.ASSERT_INCLUDED_OUTBOUND_TROLLEY)
        if included_outbound_trolley.count() == 0:
            raise Exception("❌ Outbound included trolley button not found in DOM at all.")
        included_outbound_trolley.wait_for(state="visible", timeout=2000)
        assert included_outbound_trolley.is_visible(), "❌ Outbound trolley button is not visible!"
        print("✅ Outbound trolley is included.")

    def assert_included_inbound_trolley(self):
        included_inbound_trolley = self._page.locator(self.ASSERT_INCLUDED_INBOUND_TROLLEY)
        if included_inbound_trolley.count() == 0:
            raise Exception("❌ Inbound included trolley button not found in DOM at all.")
        included_inbound_trolley.wait_for(state="visible", timeout=20000)
        assert included_inbound_trolley.is_visible(), "❌ Inbound trolley button is not visible!"
        print("✅ Inbound trolley is included.")

    def continue_to_next_page_with_recovery(
            self,
            contact_first_name, contact_last_name, passenger_first_name, passenger_last_name,
            email, verify_email, phone_number, birthday_date, passport_number, passport_expiration_date,
            attempt=1
    ):
        MAX_ATTEMPTS = 2

        self._page.wait_for_timeout(2000)
        continue_btn = self._page.locator(self.PASSENGER_CONTINUE_BTN)
        continue_btn.wait_for(state="visible", timeout=10000)
        assert continue_btn.is_visible(), "❌ 'Continue' button not found on passenger page!"

        scroll_y_before = self._page.evaluate("() => window.scrollY")
        url_before = self._page.url

        self.click(continue_btn)
        print(f"➡️ Clicked 'Continue', attempt {attempt} of {MAX_ATTEMPTS}...")
        self._page.wait_for_timeout(3000)

        scroll_y_after = self._page.evaluate("() => window.scrollY")
        url_after = self._page.url

        if scroll_y_after < scroll_y_before - 100 and url_before == url_after:
            print("🛑 Page scrolled up but did not advance – triggering recovery...")

            if attempt >= MAX_ATTEMPTS:
                self.capture_debug_info()
                raise Exception(f"❌ Still stuck after {MAX_ATTEMPTS} attempts – aborting.")

            self.capture_debug_info()

            print("🔄 Reloading page...")
            self._page.reload()
            self._page.wait_for_load_state("load")

            contact_first_name_field = self._page.locator(self.CONTACT_FIRST_NAME_FIELD)
            if contact_first_name_field.is_visible():
                print("📝 Contact page detected again – refilling form and retrying...")
                self.fill_contact_info(contact_first_name, contact_last_name, email, verify_email, phone_number)

                if self._page.locator(self.PASSENGER_FIRST_NAME_FIELD).is_visible():
                    print("✅ Passenger page loaded automatically – skipping button click.")
                else:
                    contact_continue_btn = self._page.locator(self.CONTACT_CONTINUE_BTN)
                    assert contact_continue_btn.is_visible(), "❌ 'Continue' button on contact page not found!"
                    self.click(contact_continue_btn)
                    print("➡️ Clicked 'Continue' on contact page.")
                    self._page.locator(self.PASSENGER_FIRST_NAME_FIELD).wait_for(state="visible", timeout=10000)

                self._page.wait_for_timeout(2000)

            print("⏳ Waiting for passenger fields to appear...")
            self._page.locator(self.PASSENGER_FIRST_NAME_FIELD).wait_for(state="visible", timeout=30000)
            self._page.locator(self.PASSENGER_LAST_NAME_FIELD).wait_for(state="visible", timeout=30000)
            self._page.locator(self.PASSENGER_BIRTHDAY_DATE).wait_for(state="visible", timeout=30000)
            self._page.locator(self.PASSENGER_GENDER_DROPDOWN).wait_for(state="visible", timeout=30000)
            print("✅ Passenger fields loaded.")

            self.fill_passenger_info(passenger_first_name, passenger_last_name, birthday_date)
            self.fill_passport_and_nationality_fields(passport_number, passport_expiration_date)
            self.add_outbound_baggage()
            self.add_inbound_baggage()

            # Try again, incrementing attempt count
            self.continue_to_next_page_with_recovery(
                contact_first_name, contact_last_name, passenger_first_name, passenger_last_name,
                email, verify_email, phone_number, birthday_date, passport_number, passport_expiration_date,
                attempt=attempt + 1
            )
        else:
            print("✅ Successfully moved to the next page.")

    def capture_debug_info(self):
        import datetime, os

        # Generate timestamp and create folder path
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        folder = r"C:\Users\Natan\Pictures\lastminute_automation\lastminute_flights_automation"
        os.makedirs(folder, exist_ok=True)

        # Take screenshot
        screenshot_path = fr"{folder}\screenshot_{timestamp}.png"
        try:
            self._page.screenshot(path=screenshot_path)
            print(f"📸 Screenshot saved to: {screenshot_path}")
        except Exception as e:
            print(f"❌ Failed to take screenshot: {e}")

        # Capture console logs
        logs = []

        def log_listener(msg):
            if msg.type in ["error", "warning"]:
                logs.append(f"{msg.type.upper()}: {msg.text}")

        try:
            self._page.on("console", log_listener)
            self._page.evaluate("() => console.warn('Console logging check')")
            self._page.wait_for_timeout(500)
        except Exception as e:
            print(f"❌ Failed to listen to console logs: {e}")

        # Save logs to file
        log_path = fr"{folder}\console_log_{timestamp}.txt"
        try:
            with open(log_path, "w", encoding="utf-8") as f:
                f.write("\n".join(logs) or "No console errors or warnings captured.")
            print(f"📝 Console log saved to: {log_path}")
        except Exception as e:
            print(f"❌ Failed to save console log: {e}")




