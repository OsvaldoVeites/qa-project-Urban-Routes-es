import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    ask_taxi_button= (By.CSS_SELECTOR, '.button.round')
    select_tariff = (By.XPATH,'//div[@class="tcard-title" and text()="Comfort"]')
    phone_field=(By.CLASS_NAME,'np-button')
    payment_method = (By.XPATH, '//div[@class="pp-text" and text()="Método de pago"]')
    comment_field = (By.ID,'comment')
    blanket_toggle_switch = (By.XPATH, '//span[contains(@class,"slider") and contains(@class,"round")]')
    ice_cream_plus = (By.XPATH,'//div[@class="counter-plus"]')
    ice_cream_counter = (By.XPATH, '//div[@class="counter-value"]')
    confirm_taxi = (By.CLASS_NAME, 'smart-button')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        WebDriverWait (self.driver,10).until(EC.visibility_of_element_located(self.from_field)).send_keys(from_address)

    def set_to(self, to_address):
        WebDriverWait (self.driver,10).until(EC.visibility_of_element_located(self.to_field)).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self,from_address,to_address):
        self.set_from(from_address)
        self.set_to (to_address)

    def click_ask_taxi_button(self):
        WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable(self.ask_taxi_button)).click()

    def select_tariff_comfort(self):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(self.select_tariff)).click()

    def click_phone_number(self):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(self.phone_field)).click()

    def click_payment_method(self):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(self.payment_method)).click()

    def set_comment_for_driver(self,comment):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(self.comment_field)).send_keys(comment)

    def add_blanket_and_tissues(self):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(self.blanket_toggle_switch)).click()

    def add_ice_cream(self):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(self.ice_cream_plus)).click()

    def get_ice_cream_counter(self):
        return self.driver.find_element(*self.ice_cream_counter).text

    def confirmation_taxi (self):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(self.confirm_taxi) ).click()

class PhoneWindow:
    phone_number = (By.ID,'phone')
    next_button = (By.XPATH, '//button[contains(text(),"Siguiente")]')
    confirm_button=(By.XPATH,'//button[contains(text(),"Confirmar")]')
    code_field= (By.ID,'code')
    def __init__(self, driver):
        self.driver = driver

    def set_phone_number(self, number_phone):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(self.phone_number)).send_keys(number_phone)

    def click_next_button(self):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(self.next_button)).click()

    def set_confirmation_code(self,confirmation_code):
        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located(self.code_field)).send_keys(confirmation_code)

    def click_confirm_button(self):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(self.confirm_button)).click()

class PaymentWindow:

    new_card=(By.XPATH,'//div[contains(@class,"pp-row")][.//div[text()="Agregar tarjeta"]]')
    card_number=(By.ID,'number')
    code_card=(By.CSS_SELECTOR,'#code.card-input')
    add_button=(By.XPATH,'//button[contains(text(),"Agregar")]')
    close_button = (By.XPATH,'//div[contains(@class,"payment-picker") and contains(@class,"open")]//button[contains(@class,"close-button")]')

    def __init__(self, driver):
        self.driver = driver

    def click_new_card(self):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(self.new_card)).click()

    def set_card_number(self,numbers_card):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(self.card_number)).send_keys(numbers_card)

    def set_code_card(self,card_number_code):
        field=WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(self.code_card))
        field.send_keys(card_number_code)
        field.send_keys(Keys.TAB)

    def set_card_info(self,numbers_card,card_number_code):
        self.set_card_number(numbers_card)
        self.set_code_card(card_number_code)

    def click_add_button(self):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(self.add_button)).click()

    def close_payment_window(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.close_button)).click()

class FindDriver:
    driver_name = (By.XPATH,'//div[@class="order-btn-group"]/div[2]')

    def __init__(self, driver):
        self.driver = driver

    def wait_for_driver(self):
        WebDriverWait(self.driver, 40).until(EC.visibility_of_element_located(self.driver_name))



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
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_order_taxi(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_ask_taxi_button()

    def test_select_tariff(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_ask_taxi_button()
        routes_page.select_tariff_comfort()

    def test_introduce_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_ask_taxi_button()
        routes_page.select_tariff_comfort()
        routes_page.click_phone_number()
        number_phone = data.phone_number
        phone_window= PhoneWindow(self.driver)
        phone_window.set_phone_number(number_phone)
        phone_window.click_next_button()
        code=retrieve_phone_code(self.driver)
        print(code)
        phone_window.set_confirmation_code(code)
        phone_window.click_confirm_button()

    def test_add_payment_method(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_ask_taxi_button()
        routes_page.select_tariff_comfort()
        routes_page.click_phone_number()
        number_phone = data.phone_number
        phone_window = PhoneWindow(self.driver)
        phone_window.set_phone_number(number_phone)
        phone_window.click_next_button()
        code = retrieve_phone_code(self.driver)
        print(code)
        phone_window.set_confirmation_code(code)
        phone_window.click_confirm_button()
        numbers_card=data.card_number
        card_code=data.card_code
        routes_page.click_payment_method()
        payment_method = PaymentWindow(self.driver)
        payment_method.click_new_card()
        payment_method.set_card_info(numbers_card,card_code)
        payment_method.click_add_button()
        payment_method.close_payment_window()

    def test_set_extras(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_ask_taxi_button()
        routes_page.select_tariff_comfort()
        routes_page.click_phone_number()
        number_phone = data.phone_number
        phone_window = PhoneWindow(self.driver)
        phone_window.set_phone_number(number_phone)
        phone_window.click_next_button()
        code = retrieve_phone_code(self.driver)
        print(code)
        phone_window.set_confirmation_code(code)
        phone_window.click_confirm_button()
        numbers_card = data.card_number
        card_code = data.card_code
        routes_page.click_payment_method()
        payment_method = PaymentWindow(self.driver)
        payment_method.click_new_card()
        payment_method.set_card_info(numbers_card, card_code)
        payment_method.click_add_button()
        payment_method.close_payment_window()
        comment=data.message_for_driver
        routes_page.set_comment_for_driver(comment)
        routes_page.add_blanket_and_tissues()
        routes_page.add_ice_cream ()
        routes_page.add_ice_cream()
        assert routes_page.get_ice_cream_counter()== "2"


    def test_order_tax_service(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_ask_taxi_button()
        routes_page.select_tariff_comfort()
        routes_page.click_phone_number()
        number_phone = data.phone_number
        phone_window = PhoneWindow(self.driver)
        phone_window.set_phone_number(number_phone)
        phone_window.click_next_button()
        code = retrieve_phone_code(self.driver)
        print(code)
        phone_window.set_confirmation_code(code)
        phone_window.click_confirm_button()
        numbers_card = data.card_number
        card_code = data.card_code
        routes_page.click_payment_method()
        payment_method = PaymentWindow(self.driver)
        payment_method.click_new_card()
        payment_method.set_card_info(numbers_card, card_code)
        payment_method.click_add_button()
        payment_method.close_payment_window()
        comment = data.message_for_driver
        routes_page.set_comment_for_driver(comment)
        routes_page.add_blanket_and_tissues()
        routes_page.add_ice_cream()
        routes_page.add_ice_cream()
        assert routes_page.get_ice_cream_counter() == "2"
        routes_page.confirmation_taxi()
        find_driver = FindDriver(self.driver)
        find_driver.wait_for_driver()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
