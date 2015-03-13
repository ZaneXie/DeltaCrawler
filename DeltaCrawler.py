__author__ = 'xiezj'
import json
import re

from Crawler import Crawler
from bs4 import BeautifulSoup


class DeltaCrawler(Crawler):
    def __init__(self, user=None):
        Crawler.__init__(self, user)
        self.step1_response = ""
        self.step2_response = ""
        self.step3_response = ""

    def login(self):
        if self.DEBUG:
            return
        data = {
            "loginpath": "",
            "usernameType": "skymiles",
            "passwordType": "PW",
            "homePg": "",
            "refreshURL": "https://zh.delta.com/",
            "username": self.user.login_name,
            "password": self.user.password,
            "rememberMe": "true",
            "BAUParams": "",
            "formNameSubmitted": "LoginMain",
            "usernm": self.user.login_name,
            "pwd": self.user.password,
            "Submit": ">",
            "rememberme": "on"
        }
        url = "https://zh.delta.com/custlogin/login.action"
        self.post(url, data)

    def load_data(self):
        # self.step1_response = self.load("https://zh.delta.com/acctactvty/getMySkymilesTrackerData.action", "step1.txt")
        # self.step2_response = self.load("https://www.delta.com/profile/index.action", "step2.txt")
        # self.step3_response = self.load("https://zh.delta.com/profile/getCustomerDo.action", "step3.txt")
        self.step1_response = self.get("https://zh.delta.com/acctactvty/getMySkymilesTrackerData.action")
        self.step2_response = self.get("https://www.delta.com/profile/index.action")
        self.step3_response = self.get("https://zh.delta.com/profile/getCustomerDo.action")

    def step1(self):
        """获取Current_miles, Current_MQM, Status

        """
        data = json.loads("".join(self.step1_response))
        self.user.current_MQM = data["loyaltyAccount"]["membershipStatusInfo"]["currentYearMqm"]["availableBalance"]
        self.user.current_miles = data['loyaltyAccount']['lifetimeMQM']
        self.user.status = data["loyaltyAccount"]["membershipStatusInfo"]["currentYearTierDesc"]

    def step2(self):
        pattern = re.compile(r"[.\s\S]*loginData.*?=.*?(\{.*?\})")
        data = None
        match = pattern.match(self.step2_response)
        if match is not None:
            data = json.loads(match.group(1))
        soup = BeautifulSoup("".join(self.step2_response))
        divs = soup.find_all("div", {"class": "greyFont interInfo"})
        self.user.day_of_birth = "\"" + divs[2].text.strip() + "\""
        self.user.gender = divs[1].text.strip()
        if data is not None:
            self.user.name = data["firstName"] + "/" + data["lastName"]
            self.user.email = data['primaryEmailAddress']

    def step3(self):
        data = json.loads("".join(self.step3_response))
        street = None
        city = None
        province = None
        try:
            street = data["customerDo"]["addresses"][0]["addressLine1"]
            city = data["customerDo"]["addresses"][0]["addressLine4"]
            province = data["customerDo"]["addresses"][0]["addressLine5"]
        except KeyError:
            pass
        self.user.address = "\"" + self.join_str([street, city, province], ",") + "\""

    def run(self):
        try:
            self.login()
            self.load_data()
            self.step1()
            self.step2()
            self.step3()
            self.user.parsed = True
        except Exception:
            pass

