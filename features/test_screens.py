from nose.tools import *

from custom_asserts import *
from web_app import *


def test_adding_one_screen_with_one_element():
    screens = Screens(None)
    screen = screens.add("Screen 1")
    screen.set_url("Url 1")
    screen.add_id_element("Element 1", "X1")


def test_adding_two_screens_with_two_elements():
    screens = Screens(None)
    screen = screens.add("Screen 1")
    screen.set_url("Url 1")
    screen.add_id_element("Element 1", "X1")
    screen.add_id_element("Element 2", "X2")
    screen = screens.add("Screen 2")
    screen.set_url("Url 1")
    screen.add_id_element("Element 1", "X1")
    screen.add_id_element("Element 2", "X2")


def test_duplicated_screen_exception():
    screens = Screens(None)
    screen = screens.add("Screen 1")
    screen.set_url("Url 1")
    screen.add_id_element("Element 1", "X1")
    assert_exception_and_message(
            DuplicatedScreenException,
            lambda: screens.add("Screen 1"),
            'Screen Screen 1 already exists',
    )


def test_duplicated_element_exception():
    screens = Screens(None)
    screen = screens.add("Screen 1")
    screen.set_url("Url 1")
    screen.add_id_element("Element 1", "X1")
    assert_exception_and_message(
            DuplicatedElementException,
            lambda: screen.add_id_element("Element 1", "X1"),
            'Element Element 1 already exists',
    )


def test_screen_not_found_exception():
    screens = Screens(None)
    screen = screens.add("Screen 1")
    screen.set_url("Url 1")
    screen.add_id_element("Element 1", "X1")
    screen.add_id_element("Element 2", "X2")
    screen = screens.add("Screen 2")
    screen.set_url("Url 1")
    screen.add_id_element("Element 1", "X1")
    screen.add_id_element("Element 2", "X2")

    assert_exception_and_message(
            ScreenNotFoundException,
            lambda: screens.get("Screen 3"),
            'Screen Screen 3 not found. Possible values: Screen 1,Screen 2',
    )


def test_element_not_found_exception():
    screens = Screens(None)
    screen = screens.add("Screen 1")
    screen.set_url("Url 1")
    screen.add_id_element("Element 1", "X1")
    screen.add_id_element("Element 2", "X2")

    assert_exception_and_message(
            ElementNotFoundException,
            lambda: screen.find_element("Element 3"),
            'Element Element 3 not found. Possible values: Element 1,Element 2',
    )