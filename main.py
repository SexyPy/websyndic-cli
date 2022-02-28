import bs4
import httpx
from lxml import etree


class WebSynDic:
    def __init__(self) -> None:
        self.session = httpx.Client()

        self.endpoint: dict = {
            "home": "https://www.websyndic.com/wv3/FR/?p=home",
            "cc": "https://www.websyndic.com/wv3/cc.php",
            "account": "https://www.websyndic.com/wv3/FR/?p=account",
            "visio01": "https://www.websyndic.com/wv3/FR/?p=visio01",
            "target": "https://www.websyndic.com/wv3/target.php",
            "valid_surf": "https://www.websyndic.com/wv3/valid_surf.php",
        }

    def get_data(self, url: str) -> dict:
        data = self.session.get(url).text

        return {
            "key": data.split("var key=")[1].split(";")[0],
            "rdi": data.split('var rdi="')[1].split('";')[0],
            "sx": 1,  # can change, not enough test yet
            "sh": 2,  # can change, not enough test yet
        }

    def login(self, email: str, password: str) -> None:
        data_temp = self.get_data(self.endpoint["home"])

        data = {
            "key": data_temp["key"],
            "target": "login",
            "rdi": "rdi",
            "login": email,
            "pass": password,
            "ol": "",
            "op": "",
            "sh": data_temp["sh"],
            "sx": data_temp["sx"],
        }

        print("Attempting to connect...")
        response_login = self.session.post(self.endpoint["cc"], data=data).text

        if response_login == "login o":
            profile = self.session.get(self.endpoint["account"]).text
            if profile.find("pseudo_span") != -1:
                profile_parse = bs4.BeautifulSoup(profile, "html.parser")

                pseudo = profile_parse.find("div", {"id": "pseudo_span"})
                print(f"Successful login as {pseudo.text}.")

        else:
            print("Error while trying to connect...")

    def make_points(self) -> None:
        visio1 = self.session.get(self.endpoint["visio01"]).text
        visio1_parse = bs4.BeautifulSoup(visio1, "html.parser")
        dom = etree.HTML(str(visio1_parse))
        p = (
            "https://www.websyndic.com/wv3/FR/"
            + dom.xpath('//*[@id="main_page"]/div[1]/div[3]/div/div/a')[0].attrib[
                "href"
            ]
        )
        self.session.get(self.endpoint["target"]).text
        p_access = self.session.get(p).text
        self.session.get(self.endpoint["target"]).text

        key = p_access.split("var key=")[1].split(";")[0]
        rv = p_access.split('["')[1].split('",')[0]
        v = p_access.split('["')[1].split('",')[1].split('"')[1].split('"]')[0]

        payload = f"key={key}&w=1.1&rv={rv}&v={v}"

        test = self.session.post(
            self.endpoint["valid_surf"],
            data=payload,
            headers={
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
            },
        )
        print(test.text)


websyndic = WebSynDic()
websyndic.login("", "")
websyndic.make_points()
