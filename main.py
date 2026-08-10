import helpers
import pages
import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no modificar: necesitamos logs de performance para recuperar el código de confirmación
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.set_capability(
            "goog:loggingPrefs",
            {"performance": "ALL"}
        )

        cls.driver = webdriver.Chrome(options=options)

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = pages.UrbanRoutesPage(self.driver)
        address_from = data.ADDRESS_FROM
        address_to = data.ADDRESS_TO
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
        routes_page.click_ask_taxi_button()

    def test_select_tariff(self):
        routes_page = pages.UrbanRoutesPage(self.driver)
        routes_page.select_tariff_comfort()
        assert routes_page.get_active_tariff_card() == 'Comfort'

    def test_introduce_phone_number(self):
        routes_page = pages.UrbanRoutesPage(self.driver)
        routes_page.click_phone_number()
        number_phone = data.PHONE_NUMBER
        phone_window= pages.PhoneWindow(self.driver)
        phone_window.set_phone_number(number_phone)
        phone_window.click_next_button()
        code= helpers.retrieve_phone_code(self.driver)
        print(code)
        phone_window.set_confirmation_code(code)
        phone_window.click_confirm_button()
        assert phone_window.get_confirmed_phone_number()== data.PHONE_NUMBER

    def test_add_payment_method(self):
        routes_page = pages.UrbanRoutesPage(self.driver)
        numbers_card=data.CARD_NUMBER
        card_code=data.CARD_CODE
        routes_page.click_payment_method()
        payment_method = pages.PaymentWindow(self.driver)
        payment_method.click_new_card()
        payment_method.set_card_info(numbers_card,card_code)
        payment_method.click_add_button()
        payment_method.close_payment_window()
        assert payment_method.get_current_payment_info() == 'Tarjeta'

    def test_add_message_for_driver(self):
        routes_page = pages.UrbanRoutesPage(self.driver)
        comment = data.MESSAGE_FOR_DRIVER
        routes_page.set_comment_for_driver(comment)
        assert routes_page.get_comment_for_driver() == data.MESSAGE_FOR_DRIVER

    def test_add_blanket_and_tissues(self):
        routes_page = pages.UrbanRoutesPage(self.driver)
        routes_page.add_blanket_and_tissues()
        assert routes_page.is_blanket_and_tissues_selected()

    def test_add_ice_creams(self):
        routes_page = pages.UrbanRoutesPage(self.driver)
        routes_page.add_ice_cream ()
        routes_page.add_ice_cream()
        assert routes_page.get_ice_cream_counter()== "2"

    def test_order_tax_service(self):
        routes_page = pages.UrbanRoutesPage(self.driver)
        routes_page.confirmation_taxi()
        find_driver = pages.FindDriver(self.driver)
        find_driver.wait_for_driver()
        assert routes_page.driver.find_element(By.CLASS_NAME, 'tariff-cards').is_displayed()

    def verify_info_driver (self):
        routes_page = pages.UrbanRoutesPage(self.driver)
        find_driver = pages.FindDriver(self.driver)
        find_driver.wait_for_driver()
        assert find_driver.driver_picture.is_displayed()
        assert find_driver.driver_raitng.is_displayed()
        assert find_driver.driver_name.is_displayed()
    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
