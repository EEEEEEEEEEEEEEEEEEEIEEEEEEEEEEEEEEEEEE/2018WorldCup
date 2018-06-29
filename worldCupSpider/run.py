import requests
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import chardet
import time as t
from datetime import datetime
from app import db
from app.models import Team, Group, Duel, TeamPinYin
import pinyin


class WorldCupSpider(object):

    def __init__(self, headers=None, proxy=None, url=None, driver=None):
        """
        定义初始化网址和存储数据库
        """
        if url is None:
            print("初始URL不能为空！启动失败..")
            return

        self.url = url

        if driver == "phantomjs":
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36")

            self.driver = webdriver.PhantomJS(executable_path="driver/phantomjs-2.1.1-windows/bin/phantomjs.exe",
                                              desired_capabilities=dcap)

        elif driver == "chrome":
            self.driver = webdriver.Chrome(executable_path="driver/chrome/chromedriver.exe")
            self.driver.implicitly_wait(10)
            self.driver.set_window_size(1366, 768)
        elif driver == "firefox":
            pass
        else:
            self.headers = headers

    def html_download_with_requests(self, url):
        print("开始下载%s" % url)
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            print("访问出错，结束...")
            return None
        response.encoding = chardet.detect(response.content)["encoding"]
        print(response.text)
        return response.text

    def html_download_with_selenium(self, url):
        self.driver.get(url)
        t.sleep(3)

    def team_match_parse_with_pyquery(self, data):
        print("开始解析...")
        doc = pq(data)
        groups = doc("#part .part")
        for group in groups:
            print(help(group))
            print(group.find_class("layout-mb-b")[0].text())

    def team_match_parse_with_webdriver(self):
        print("开始解析")
        data_list = []
        parts = self.driver.find_elements_by_css_selector("#part .part")
        for part in parts:
            group_name = part.find_element_by_css_selector(".title-c.layout-mb-b").text
            print(group_name)
            group_list = part.find_elements_by_css_selector("table tr")
            for row in group_list[1:]:
                datetime_str = row.find_element_by_css_selector("td:nth-child(1)").text.split(" ")[0]
                datetime_str += row.find_element_by_css_selector("td:nth-child(2)").text
                v1 = row.find_element_by_css_selector("td:nth-child(3) span:first-child").text
                try:
                    vs = WebDriverWait(row, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(3) span:nth-child(2)")))
                finally:
                    pass
                try:
                    v2 = WebDriverWait(row, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(3) span:nth-child(3)")))
                finally:
                    pass
                group_cls = row.find_element_by_css_selector("td:nth-child(4)").text
                area = row.find_element_by_css_selector("td:nth-child(5)").text
                data = dict(group_name=group_name,
                            datetime=datetime.strptime(datetime_str + " 2018", "%m月%d日%H:%M %Y"),
                            v1=v1,
                            vs=vs.text,
                            v2=v2.text,
                            group_cls=group_cls,
                            area=area
                            )
                print(data)
                data_list.append(data)

        return data_list

    def team_match_storage(self, data):
        for d in data:
            group = Group.query.filter_by(name=d["group_name"]).first()
            if group is None:
                group = Group(name=d["group_name"])
                db.session.add(group)
            v1 = Team.query.filter_by(name=d["v1"]).first()
            if v1 is None:
                v1 = Team(name=d["v1"], group=group)
                v1_pinyin = TeamPinYin(name=pinyin.get(d["v1"], format="strip"), team=v1)
                db.session.add(v1)
                db.session.add(v1_pinyin)
            v2 = Team.query.filter_by(name=d["v2"]).first()
            if v2 is None:
                v2 = Team(name=d["v2"], group=group)
                v2_pinyin = TeamPinYin(name=pinyin.get(d["v2"], format="strip"), team=v2)
                db.session.add(v2)
                db.session.add(v2_pinyin)
            db.session.commit()
            duel = Duel(team_er=v1, team_ed=v2, t1_score=d["vs"][0], t2_score=d["vs"][2], datetime=d["datetime"],
                        area=d["area"], group_cls=d["group_cls"])
            db.session.add(duel)
            db.session.commit()
            print("保存%s小组赛成功..." % d["group_name"])

    def score_parse_with_webdriver(self):
        print("开始解析球队信息....")
        data_list = []
        groups = self.driver.find_elements_by_css_selector(".group")
        print("groups len:", len(groups))
        for group in groups:
            teams = group.find_elements_by_css_selector("tr")
            for team in teams[1:]:
                team_name = WebDriverWait(team, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(2)")))
                session = WebDriverWait(team, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(3)")))
                victory = WebDriverWait(team, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(4)")))
                flat = WebDriverWait(team, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(5)")))
                lost = WebDriverWait(team, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(6)")))
                goal = WebDriverWait(team, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(7)")))
                fumble = WebDriverWait(team, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(8)")))
                gd = WebDriverWait(team, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(9)")))
                integral = WebDriverWait(team, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(10)")))
                data = dict(team_name=team_name.text,
                            session=session.text,
                            victory=victory.text,
                            flat=flat.text,
                            lost=lost.text,
                            goal=goal.text,
                            fumble=fumble.text,
                            gd=gd.text,
                            integral=integral.text)
                print(data)
                data_list.append(data)
        return data_list

    def score_storage(self, data):
        print("开始保存球队信息...")
        for d in data:
            team = Team.query.filter_by(name=d["team_name"]).first()
            if team is None:
                print("球队名称错误，没有该球队:%s" % d["team_name"])
                return
            team.session = d["session"]
            team.victory = d["victory"]
            team.flat = d["flat"]
            team.lost = d["lost"]
            team.goal = d["goal"]
            team.fumble = d["fumble"]
            team.gd = d["gd"]
            team.integral = d["integral"]
            db.session.add(team)
            db.session.commit()
            print("保存%s小组信息成功..." % d["team_name"])
            print(team.name, team.session, team.victory,
                  team.flat, team.lost, team.goal, team.fumble, team.gd, team.integral)

    def run(self):
        db.create_all()
        self.html_download_with_selenium(self.url)
        data = self.team_match_parse_with_webdriver()
        self.team_match_storage(data)
        self.url = url_2
        self.html_download_with_selenium(self.url)
        data = self.score_parse_with_webdriver()
        self.score_storage(data)

    def driver_quit(self):
        self.driver.quit()


if __name__ == '__main__':
    url_1 = "http://2018.sina.com.cn/schedule/group.shtml"
    url_2 = "http://2018.sina.com.cn/scoreboard/page.shtml"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"
    }
    spider = WorldCupSpider(url=url_1, headers=header, driver="chrome")
    spider.run()
