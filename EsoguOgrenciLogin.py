#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import getpass
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of

class EsoguLogin(unittest.TestCase):
    def setUp(self):
        # Get username and password
        self.username = input('Ogrenci Numaraniz: ')
        self.password = getpass.getpass('Sifre: ')

        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)
        self.browser.maximize_window()

    def tearDown(self):
        self.browser.quit()

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.browser.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.browser, timeout).until(
            staleness_of(old_page)
        )

    def test_can_login_into_server(self):
        self.browser.get('http://esogubsweb1.ogu.edu.tr:7777')

        with self.wait_for_page_load(timeout=10):
            # choose top frame in order to get the form elements
            self.browser.switch_to.frame("frame_giris_baslik")

            # get the username input by xpath
            username_xpath = "//input[@name='param01']"
            username = self.browser.find_element_by_xpath(username_xpath)

            # get the password input by xpath
            pass_xpath = "//input[@name='param02']"
            password = self.browser.find_element_by_xpath(pass_xpath)

            # write them into input boxes
            username.send_keys(self.username)
            password.send_keys(self.password)

            # find the submit link
            span_element = self.browser.find_element_by_partial_link_text('Giriş')
            span_element.click()

            # OK We are logged in now choose the top frame again
            self.browser.switch_to.frame("frame_giris_baslik")

            # Open "Sinav Sonuc" menu
            sinav_sonuc = self.browser.find_element_by_link_text("Sınav Sonuç")
            sinav_sonuc.click()

            import time
            time.sleep(600) #This needs to be fixed with more proper way

if __name__ == '__main__':
    unittest.main()
