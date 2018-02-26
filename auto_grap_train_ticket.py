# -*- coding: utf-8 -*-
_author_ = '$陈吉-一颗小洋葱啊'

import traceback
import time, sys
from splinter.browser import Browser
from time import sleep

class Booking(object):
    login_url = 'https://kyfw.12306.cn/otn/login/init'
    my_login_url = 'https://kyfw.12306.cn/otn/index/initMy12306'
    tickets_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
    browser_driver_name = 'firefox'
    executable_path = 'D:\Python3.6.3\BrowserDriver\geckodriver.exe'

    def __init__(self, username, password, departure, destination, date, trip, passenger, seat):
        self.username = username
        self.password = password
        self.departure = departure
        self.destination = destination
        self.date = date
        self.trip = trip
        self.passenger = passenger
        self.seat = seat

    def login(self):
        self.browser.visit(self.login_url)
        self.browser.fill('loginUserDTO.user_name', self.username)
        self.browser.fill('userDTO.password', self.password)
        print('手动输入验证码。')
        while True:
            if self.browser.url != self.my_login_url:
                sleep(0.5)
            else:
                break
        print('登录12306成功！')

    def place_order(self):
        self.browser = Browser(driver_name = self.browser_driver_name, executable_path = self.executable_path)
        self.browser.driver.set_window_size(1200, 700)
        self.login()
        self.browser.visit(self.tickets_url)
        print('开始查询并购票：')
        try:
            self.browser.cookies.add({"_jc_save_fromStation": self.departure})
            self.browser.cookies.add({"_jc_save_toStation": self.destination})
            self.browser.cookies.add({"_jc_save_fromDate": self.date})
            self.browser.reload()

            count = 0
            if self.trip != 0:
                while self.browser.url == self.tickets_url:
                    self.browser.find_by_text("查询").click()
                    count += 1
                    print('第%d次查询。' % count)
                    try:
                        self.browser.find_by_text("预订")[self.trip - 1].click()
                        sleep(0.1)
                    except Exception as e:
                        print(e)
                        print('指定车次方式订票，所预订车次已无票，无法预订！')
                        continue
            else:
                while self.browser.url == self.tickets_url:
                    self.browser.find_by_text("查询").click()
                    count += 1
                    print('第%d次查询。' % count)
                    try:
                        for i in self.browser.find_by_text("预订"):
                            i.click()
                            sleep(0.1)
                    except Exception as e:
                        print(e)
                        print('不指定车次方式订票，所预订车次已无票，无法预订！')
                        continue
            print('已找到车次，开始订票：')
            sleep(0.5)
            print('选择乘车人、席别：')
            for pasger in self.passenger:
                self.browser.find_by_text(pasger).last.click()
            	if pasger[-1] == ')':
                	self.browser.find_by_id('dialog_xsertcj_ok').click()
                	#sleep(0.1)
                	#self.browser.find_by_text(self.seat).last.click()
                	sleep(0.3)
            print('提交订单！')
            self.browser.find_by_id('submitOrder_id').click()
            sleep(0.5)
            print('确认')
            self.browser.find_by_id('qr_submit_id').click()
            print('车票预订成功，等待付款！')
        except Exception as e:
            print(e)
            print('选择乘车人、席别时出错，车票预定失败！')

if __name__ == '__main__':
    username = '189****7809'
    password = '0123456'
    departure = '%u6500%u679D%u82B1%2CPRW'
    destination = '%u9686%u660C%2CLCW'
    date = '2018-02-08'
    trip = 0
    passenger = ['陈']
    seat = '硬卧'
    booking_tickets=Booking(username, password, departure, destination, date, trip, passenger, seat)
    booking_tickets.place_order()




