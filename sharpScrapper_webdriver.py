# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class SharpScrapperWebdriver(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://sharp.direct.gov.uk/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_sharp_scrapper_webdriver(self):
        driver = self.driver
        # nextSearchPage = self.base_url + "testhelmetlist?sharp-make=All&sharp-model=&sharp-type=2&sharp-rating=1"
        nextSearchPage = "http://sharp.direct.gov.uk/testhelmetlist?page=6&sharp-make=All&sharp-model=&sharp-type=All&sharp-rating=1&sharp-price-from=0&sharp-price-to=9999&discontinued=1"

        while nextSearchPage:
            driver.get(nextSearchPage)
            nextSearchPage = self.getElement('xpath', "//li[contains(@class, 'pager-next')]//a")
            if nextSearchPage:
                nextSearchPage = nextSearchPage.get_attribute('href')

            links = []
            for link in driver.find_elements_by_xpath("//table[@id='search-results']//tr/td[2]/a"):
                link = link.get_attribute('href')
                links.append(link)

            for link in links:
                driver.get(link)

                makeModel = self.getElement('xpath', "//div[@id='content']/div[1]/h1")
                if makeModel:
                    makeModel = makeModel.text

                dts = driver.find_elements_by_xpath("//div[contains(@class,'helmet-details')]/dl/dt")
                dds = driver.find_elements_by_xpath("//div[contains(@class,'helmet-details')]/dl/dd")

                modelType = ''
                kg        = '0.00'
                price     = '0.00'
                material  = 'Polycarbonate'
                rating    = '1'

                for i in range(0,len(dts)):
                    dtText = dts[i].text
                    if 'Type' in dtText:
                        modelType = dds[i].text
                    elif 'Weight' in dtText:
                        kg     = dds[i].text
                        if 'kg' in kg:
                            kg = kg.replace('kg','')
                    elif 'Price' in dtText:
                        price     = dds[i].text

                m  = self.getElement('xpath', "//ul[contains(@class,'materials')]/li")
                if m:
                    material = m.text

                r    = self.getElement('xpath', "//img[@id='rating-image']")
                if r:
                    rating = r.get_attribute('alt')
                    if rating:
                        rating = rating.strip()[0]

                print makeModel,',', modelType,',', kg,',', price,',', material,',', rating,',',link

        print 'got all the pages i could :)'
    
    def getElement(self, how, what):
        try: return self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
