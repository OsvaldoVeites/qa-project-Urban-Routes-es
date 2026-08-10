from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    ask_taxi_button= (By.CSS_SELECTOR, '.button.round')
    select_tariff = (By.XPATH,'//div[@class="tcard-title" and text()="Comfort"]')
    active_tariff_card = (By.XPATH, '//div[@class="tcard active"]//div[@class="tcard-title"]')
    phone_field=(By.CLASS_NAME,'np-button')
    confirmed_phone_number = (By.CLASS_NAME, 'np-text')
    payment_method = (By.XPATH, '//div[@class="pp-text" and text()="Método de pago"]')
    comment_field = (By.ID,'comment')
    blanket_toggle_switch = (By.XPATH, '//span[contains(@class,"slider") and contains(@class,"round")]')
    blanket_toggle_switch_selected = (By.XPATH, '//div[contains(@class,"switch")]//input[@type="checkbox"]')
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

    def get_active_tariff_card (self):
        return self.driver.find_element(*self.active_tariff_card).text

    def click_phone_number(self):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(self.phone_field)).click()

    def click_payment_method(self):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(self.payment_method)).click()

    def set_comment_for_driver(self,comment):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(self.comment_field)).send_keys(comment)

    def get_comment_for_driver(self):
        return self.driver.find_element(*self.comment_field ).get_attribute("value")

    def add_blanket_and_tissues(self):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(self.blanket_toggle_switch)).click()

    def is_blanket_and_tissues_selected(self):
        return self.driver.find_element(*self.blanket_toggle_switch_selected).is_selected()

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
    confirmed_phone_number = (By.CLASS_NAME, 'np-text')

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

    def get_confirmed_phone_number(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.confirmed_phone_number)).text

class PaymentWindow:

    new_card=(By.XPATH,'//div[contains(@class,"pp-row")][.//div[text()="Agregar tarjeta"]]')
    card_number=(By.ID,'number')
    code_card=(By.CSS_SELECTOR,'#code.card-input')
    add_button=(By.XPATH,'//button[contains(text(),"Agregar")]')
    close_button = (By.XPATH,'//div[contains(@class,"payment-picker") and contains(@class,"open")]//button[contains(@class,"close-button")]')
    current_payment_info = (By.CLASS_NAME, 'pp-value-text')

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

    def get_current_payment_info(self):
        return self.driver.find_element (*self.current_payment_info).text


class FindDriver:
    driver_name = (By.XPATH,'//div[@class="order-btn-group"]/div[2]')
    driver_raitng = (By.CLASS_NAME,'order-btn-rating')
    driver_picture = (By.CSS_SELECTOR,'img[src="/static/media/bender.e90e5089.svg"]')
    def __init__(self, driver):
        self.driver = driver

    def wait_for_driver(self):
        WebDriverWait(self.driver, 40).until(EC.visibility_of_element_located(self.driver_name))
