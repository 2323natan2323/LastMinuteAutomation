from time import sleep

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from enum import Enum
from typing import Optional, Union

from playwright.sync_api import Page, Locator
from lastminute_co_il_flights_automation.pages.base_page import BasePage


class BaggageStatus(Enum):
    INCLUDED = "Included"
    ADDABLE = "Addable"
    NOT_INCLUDED = "Not included"

class TrolleyStatus(Enum):
    INCLUDED = "Included"
    ADDABLE = "Addable"
    NOT_INCLUDED = "Not included"

class FlexiPage(BasePage):

    FLEXI_PAGE_ELEMENT = ".step-button.current > .btn-title"
    FLEXI_BTN = ".option-card-container.premium .call-to-action button"
    OUTBOUND_FLIGHT_DIRECT_OPTION = 'app-flight-card .flight-row:nth-child(1) [key="Flights.Direct"]'
    INBOUND_FLIGHT_DIRECT_OPTION = 'app-flight-card .flight-row:nth-child(2) [key="Flights.Direct"]'
    OUTBOUND_FLIGHT_STOP_OPTION = 'app-flight-card .flight-row:nth-child(1) .stops'
    INBOUND_FLIGHT_STOP_OPTION = 'app-flight-card .flight-row:nth-child(2) .stops'

    OUTBOUND_ADDABLE_BAGGAGE = (
        '.flights-container > .flight-row:nth-child(1) '
        '.baggage-row.equal-width-section:nth-child(2)'
        ':has(span:nth-child(3):visible:has-text("הוספה בהמשך")) '
        '.quantity:visible:has-text("0")'
    )

    INBOUND_ADDABLE_BAGGAGE = (
        '.flights-container > .flight-row:nth-child(2) '
        '.baggage-row.equal-width-section:nth-child(2)'
        ':has(span:nth-child(3):visible:has-text("הוספה בהמשך")) '
        '.quantity:visible:has-text("0")'
    )

    OUTBOUND_INCLUDED_BAGGAGE = (
        '.flights-container > .flight-row:nth-child(1) '
        '.baggage-row.equal-width-section:nth-child(2) '
        '.quantity:visible:has-text("1"), '
        '.flights-container > .flight-row:nth-child(1) '
        '.baggage-row.equal-width-section:nth-child(2) '
        '.quantity:visible:has-text("2")'
    )

    INBOUND_INCLUDED_BAGGAGE = (
        '.flights-container > .flight-row:nth-child(2) '
        '.baggage-row.equal-width-section:nth-child(2) '
        '.quantity:visible:has-text("1"), '
        '.flights-container > .flight-row:nth-child(2) '
        '.baggage-row.equal-width-section:nth-child(2) '
        '.quantity:visible:has-text("2")'
    )

    OUTBOUND_NOT_INCLUDED_BAGGAGE = (
        '.flights-container > .flight-row:nth-child(1) '
        '.baggage-row.equal-width-section:nth-child(2)'
        ':has(span:nth-child(2):visible:has-text("לא כלולה"))'
        ':has(span:nth-child(1):visible:has-text("0"))'
    )

    INBOUND_NOT_INCLUDED_BAGGAGE = (
        '.flights-container > .flight-row:nth-child(2) '
        '.baggage-row.equal-width-section:nth-child(2)'
        ':has(span:nth-child(2):visible:has-text("לא כלולה"))'
        ':has(span:nth-child(1):visible:has-text("0"))'
    )

    OUTBOUND_INCLUDED_TROLLEY = (
        '.flights-container > .flight-row:nth-child(1) .baggage-row.last-child .quantity:visible:has-text("1"), '
        '.flights-container > .flight-row:nth-child(1) .baggage-row.last-child .quantity:visible:has-text("2")'
    )

    INBOUND_INCLUDED_TROLLEY = (
        '.flights-container > .flight-row:nth-child(2) .baggage-row.last-child .quantity:visible:has-text("1"), '
        '.flights-container > .flight-row:nth-child(2) .baggage-row.last-child .quantity:visible:has-text("2")'
    )

    OUTBOUND_ADDABLE_TROLLEY = (
        '.flights-container > .flight-row:nth-child(1) .baggage-row.last-child'
        ':has(.with-upgrade-option:visible:has-text("הוספה בהמשך")):has(.quantity:visible:has-text("0"))'
    )

    INBOUND_ADDABLE_TROLLEY = (
        '.flights-container > .flight-row:nth-child(2) .baggage-row.last-child'
        ':has(.with-upgrade-option:visible:has-text("הוספה בהמשך"))'
        ':has(.quantity:visible:has-text("0"))'
    )

    OUTBOUND_NOT_INCLUDED_TROLLEY = (
        '.flights-container > .flight-row:nth-child(1) .baggage-row.last-child'
        ':has(.text-value:visible:has-text("לא כלולה")):has(.quantity:visible:has-text("0"))'
    )

    INBOUND_NOT_INCLUDED_TROLLEY = (
        '.flights-container > .flight-row:nth-child(2) .baggage-row.last-child'
        ':has(.text-value:visible:has-text("לא כלולה")):has(.quantity:visible:has-text("0"))'
    )


    def __init__(self, page: Page):
        super().__init__(page)
        self.outbound_baggage_status = None
        self.inbound_baggage_status = None
        self.outbound_trolley_status = None
        self.inbound_trolley_status = None

    def wait_for_page_to_load(self):
        self._page.wait_for_load_state("load")  # מחכה לטעינת ה-HTML והמשאבים הראשוניים
        self._page.wait_for_load_state("networkidle")  # מחכה שהרשת תתייצב (אין בקשות פתוחות)
        print("🌐 Waiting for Flexi page to load...")

        flexi_page_element = self._page.locator(self.FLEXI_PAGE_ELEMENT)
        try:
            flexi_page_element.wait_for(state="visible", timeout=40000)
            print("✅ Flexi page loaded successfully.")
        except PlaywrightTimeoutError:
            raise AssertionError("❌ Flexi page did not load after 40 seconds!")

        # המתנה קצרה נוספת כדי לאפשר עדכוני JS פנימיים בדף
        self._page.wait_for_timeout(3000)  # 3 שניות
        print("⏳ Extra wait completed (3 seconds).")


    def choose_flexi_ticket(self):
        flexi_btn = self._page.locator(self.FLEXI_BTN)
        flexi_btn.wait_for(state= "visible", timeout=20000)

        assert flexi_btn.is_visible(), "❌ Flexi ticket button was not found!"
        print("✅ Flexi ticket button is visible. Clicking now...")
        self.click(flexi_btn)

    def get_baggage_status(self,
                           included_locator: Locator,
                           addable_locator: Locator,
                           not_included_locator: Locator):

        if included_locator.is_visible():
            print("✅ Included baggage is visible.")
            return BaggageStatus.INCLUDED.value

        if addable_locator.is_visible():
            print("✅ Addable baggage is visible.")
            return BaggageStatus.ADDABLE.value

        if not_included_locator.is_visible():
            print("✅ Not included baggage is visible.")
            return BaggageStatus.NOT_INCLUDED.value

        print("❌ No baggage status has been received.")
        return None

    def get_trolley_status(self,
                           included_locator: Locator,
                           addable_locator: Locator,
                           not_included_locator: Locator):

        if included_locator.is_visible():
            print("✅ Included trolley is visible.")
            return TrolleyStatus.INCLUDED.value

        if addable_locator.is_visible():
            print("✅ Addable trolley is visible.")
            return TrolleyStatus.ADDABLE.value

        if not_included_locator.is_visible():
            print("✅ Not included trolley is visible.")
            return TrolleyStatus.NOT_INCLUDED.value

        print("❌ No trolley status has been received.")
        return None

    def save_outbound_baggage_status(self):
        self.outbound_baggage_status = self.get_baggage_status(
        self._page.locator(self.OUTBOUND_INCLUDED_BAGGAGE),
        self._page.locator(self.OUTBOUND_ADDABLE_BAGGAGE),
        self._page.locator(self.OUTBOUND_NOT_INCLUDED_BAGGAGE)
        )


    def save_inbound_baggage_status(self):
        self.inbound_baggage_status = self.get_baggage_status(
        self._page.locator(self.INBOUND_INCLUDED_BAGGAGE),
        self._page.locator(self.INBOUND_ADDABLE_BAGGAGE),
        self._page.locator(self.INBOUND_NOT_INCLUDED_BAGGAGE)
        )


    def save_outbound_trolley_status(self):
        self.outbound_trolley_status = self.get_trolley_status(
        self._page.locator(self.OUTBOUND_INCLUDED_TROLLEY),
        self._page.locator(self.OUTBOUND_ADDABLE_TROLLEY),
        self._page.locator(self.OUTBOUND_NOT_INCLUDED_TROLLEY)
        )

    def save_inbound_trolley_status(self):
        self.inbound_trolley_status = self.get_trolley_status(
        self._page.locator(self.INBOUND_INCLUDED_TROLLEY),
        self._page.locator(self.INBOUND_ADDABLE_TROLLEY),
        self._page.locator(self.INBOUND_NOT_INCLUDED_TROLLEY)
        )

    def save_all_lugagge_info(self):
        self.save_outbound_baggage_status()
        print("📦 outbound baggage:", self.outbound_baggage_status)

        self.save_inbound_baggage_status()
        print("📦 inbound baggage:", self.inbound_baggage_status)

        self.save_outbound_trolley_status()
        print("🧳 outbound trolley:", self.outbound_trolley_status)

        self.save_inbound_trolley_status()
        print("🧳 inbound trolley:", self.inbound_trolley_status)


    # def get_flight_info(self):
    #     flight_info: dict[str, Optional[str]] = {
    #         "outbound": None,
    #         "inbound": None,
    #         "flight_combination": None,
    #     }
    #
    #     # 🛫 זיהוי טיסת הלוך
    #     if self._page.locator(self.OUTBOUND_FLIGHT_DIRECT_OPTION).is_visible(timeout=3000):
    #         flight_info["outbound"] = "Direct"
    #     elif self._page.locator(self.OUTBOUND_FLIGHT_STOP_OPTION).is_visible(timeout=3000):
    #         stops_text = self._page.locator(self.OUTBOUND_FLIGHT_STOP_OPTION).inner_text().strip()
    #         if "1" in stops_text:
    #             flight_info["outbound"] = "1 Stop"
    #         elif "2" in stops_text:
    #             flight_info["outbound"] = "2 Stops"
    #
    #     # 🛬 זיהוי טיסת חזור
    #     if self._page.locator(self.INBOUND_FLIGHT_DIRECT_OPTION).is_visible(timeout=3000):
    #         flight_info["inbound"] = "Direct"
    #     elif self._page.locator(self.INBOUND_FLIGHT_STOP_OPTION).is_visible(timeout=3000):
    #         stops_text = self._page.locator(self.INBOUND_FLIGHT_STOP_OPTION).inner_text().strip()
    #         if "1" in stops_text:
    #             flight_info["inbound"] = "1 Stop"
    #         elif "2" in stops_text:
    #             flight_info["inbound"] = "2 Stops"
    #
    #
    #     # 🧠 קביעת שילוב הטיסות
    #     if flight_info["outbound"] and flight_info["inbound"]:
    #         combination_key = f"{flight_info['outbound']}_{flight_info['inbound']}".replace(" ", "_")
    #         try:
    #             flight_info["flight_combination"] = FlightCombination[combination_key].value
    #         except KeyError:
    #             print(f"⚠️ Unknown flight combination: {combination_key}")
    #             flight_info["flight_combination"] = None
    #
    #     print("Flight Info:", flight_info)
    #     return flight_info
    #
