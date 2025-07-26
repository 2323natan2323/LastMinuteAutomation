from lastminute_co_il_flights_automation.pages.page1_home_page import HomePage
from lastminute_co_il_flights_automation.pages.page2_search_results_page import \
    SearchResultsPage
from lastminute_co_il_flights_automation.pages.page3_flexi_page import FlexiPage
from lastminute_co_il_flights_automation.pages.page4_contact_page import ContactPage
from lastminute_co_il_flights_automation.pages.page5_general_services_page import \
    AncillariesPage
from lastminute_co_il_flights_automation.pages.page6_flight_summary_details import \
    FlightSummaryDetails


class BaseTest:
    def init_pages(self, main_page, new_tab=None):
        self.home_page = HomePage(main_page)
        self.search_results_page = SearchResultsPage(main_page)

        if new_tab:
            self.flexi = FlexiPage(new_tab)
            self.contact = ContactPage(new_tab)
            self.ancillaries = AncillariesPage(new_tab)
            self.summary = FlightSummaryDetails(new_tab)
