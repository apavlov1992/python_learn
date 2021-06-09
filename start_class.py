#!/usr/bin/env python3

import sys
from selenium import webdriver

# Define variables
driver = webdriver.Chrome("/Users/a.pavlov/Downloads/chromedriver")
driver.get("https://lk.sut.ru/cabinet/")
user_name = driver.find_element_by_name('users')
passwd = driver.find_element_by_name('parole')
users = driver.find_element_by_name('users')
parole = driver.find_element_by_name('parole')


students_credentials = {
    'login': 'password',
}


class Click:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def click_button(self):
        users.send_keys(self.name)
        parole.send_keys(self.password)
        driver.find_element_by_name('logButton').click()


def __main__():
    for name, password in students_credentials.items():
        a = Click(name, password)
        a.click_button()


if __name__ == '__main__':
    sys.exit(__main__())