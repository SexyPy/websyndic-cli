import bs4
import httpx


class WebSynDic:
    def __init__(self) -> None:
        self.site: str = "https://www.websyndic.com/"
        self.session = httpx.Client()

        self.endpoint: dict = {
            "cc": "https://www.websyndic.com/wv3/cc.php",
            "account": "https://www.websyndic.com/wv3/FR/?p=account",
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
        data_temp = self.get_data(self.site)

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


WebSynDic().login("", "")
