from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Amazon_API:
    state = ""

    def __init__(self,width=1151,height=629):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ( "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:36.0) Gecko/20100101 Firefox/36.0 WebKit" )
        self.br = webdriver.PhantomJS(desired_capabilities=dcap,service_args=['--ssl-protocol=any','--ignore-ssl-errors=true'])
        self.br.set_window_size(width,height)
        self.state = "init"

    def login_from_main(self,username,password):
        br =  self.br
        self.br.get("https://www.amazon.com/")
        href = br.find_element_by_xpath("//div[@id='nav-flyout-ya-signin']/a").get_attribute("href")
        br.get(href)
        self.state = "login_from_main"
        self.login(username,password)

    def login(self,username,password):
        self.state = "login"
        br = self.br
        br.find_element_by_id("ap_email").send_keys(username)
        br.find_element_by_id("ap_password").send_keys(password)
        br.find_element_by_id("signInSubmit").send_keys(Keys.ENTER)
        self.state = "loggedin"

    def enter_code(self,code):
        if self.state=="loggedin":
            br = self.br
            br.find_element_by_partial_link_text("Gift Cards").click()
            redeem = [(i,i.get_attribute("alt")) for i in self.br.find_elements_by_xpath("//div[@id='merchandised-content']//map/area[@alt]") if i.get_attribute("alt")=='Redeem an Amazon.com gift card']
            if redeem:
                redeem[0][0].click()
                br.find_element_by_id("gc-redemption-input").send_keys(code)
                br.find_elements_by_class_name("a-button-input")[0].click()
                if "GC claim code is invalid" in br.page_source:
                    return (code,br.page_source,False)
                else:
                    return (code,br.page_source,True)
        else:
            return ("not_loggen_in",self.br.page_source,False)

    def run(self,username,password,code):
        br = self.br
        br.delete_all_cookies()
        self.login_from_main(username,password)
        return self.enter_code(code)

