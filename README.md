# QA Project - Urban Routes

## Descripción

Proyecto de automatización de pruebas para comprobar la funcionalidad de Urban Routes.

Las pruebas fueron diseñadas de acuerdo con la lista de comprobación proporcionada y se implementaron utilizando el patrón Page Object Model (POM).

## Requisitos

Para ejecutar las pruebas es necesario tener instalados:

- Python
- pytest
- selenium

## Ejecución de las pruebas

Para ejecutar todas las pruebas, utiliza: pytest

-Los datos necesarios para solicitar el servicio se encuentran en: data.py

## Automatización

Se utilizó la herramienta DevTools del navegador para identificar y obtener los diferentes localizadores utilizados en las pruebas.

Se definieron diferentes clases de acuerdo con la lógica y los componentes de la aplicación:
- Page Objects
- UrbanRoutesPage
- PhoneWindow
- PaymentWindow
- FindDriver

Cada clase contiene los localizadores y métodos correspondientes a la sección de la aplicación que representa.

## Pruebas

Las pruebas se definieron en la clase:

TestUrbanRoutes

Pruebas implementadas:

- test_set_route() : Comprueba la configuración de la ruta.
- test_order_taxi() : Comprueba la solicitud de un taxi.
- test_select_tariff() : Comprueba la selección de la tarifa Comfort.
- test_introduce_phone_number() : Comprueba la introducción y confirmación del número telefónico.
- test_add_payment_method() : Comprueba la adición de un método de pago.
- test_set_extras() : Comprueba la selección de servicios adicionales.
- test_order_tax_service() : Comprueba el proceso completo de solicitud del servicio.

