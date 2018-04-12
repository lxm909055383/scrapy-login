# -*- coding: utf-8 -*-
import scrapy
import urllib.request
from PIL import Image

class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['douban.com']
    # start_urls = ['http://https://www.douban.com//']
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

    def start_requests(self):
        #请求登陆界面
        return [scrapy.FormRequest("https://accounts.douban.com/login", headers=self.headers, meta={"cookiejar": 1}, callback=self.parse_before_login)]

    def parse_before_login(self, response):
        print("登录前表单填充")
        #验证码编号
        captcha_id = response.xpath('//input[@name="captcha-id"]/@value').extract_first()
        # 验证码图片链接
        captcha_image_url = response.xpath('//img[@id="captcha_image"]/@src').extract_first()
        if captcha_image_url is None:
            print("登录时无验证码")
            formdata = {
                "source": "index_nav",
                "form_email": "909055383@qq.com",
                "form_password": "***",
            }
        else:
            print("登录时有验证码")
            save_image_path = r"D:\all of lxm\to github\douban_login\captcha.jpeg"
            # 将图片验证码下载到本地
            urllib.request.urlretrieve(captcha_image_url, save_image_path)
            # 打开图片，以便我们识别图中验证码
            try:
                im = Image.open('captcha.jpeg')
                im.show()
            except:
                pass
            # 手动输入验证码
            captcha_solution = input('根据打开的图片输入验证码:')
            formdata = {
                "source": "None",
                "redir": "https://www.douban.com",
                "form_email": "909055383@qq.com",
                "form_password": "***",
                "captcha-solution": captcha_solution,
                "captcha-id": captcha_id,
                "login": "登录",
            }

        print("登录中")
        # 提交表单
        return scrapy.FormRequest.from_response(response, meta={"cookiejar": response.meta["cookiejar"]}, headers=self.headers, formdata=formdata, callback=self.parse_after_login)

    def parse_after_login(self, response):
        account = response.xpath('//a[@class="bn-more"]/span/text()').extract_first()
        if account is None:
            print("登录失败")
        else:
            print(u"登录成功,当前账户为 %s" % account)
