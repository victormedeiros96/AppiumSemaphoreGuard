from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from device_control.device_control import DeviceControl

class AppiumDriverBasic:
    def __init__(self, server_ip, server_port, desired_capabilities):
        self.desired_capabilities = desired_capabilities
        self.server_ip = (server_ip, server_port)
        self.device_control = DeviceControl()

    @property
    def IOS(self):
        return self.desired_capabilities['platformName'] == 'IOS'

    @property
    def Android(self):
        return self.desired_capabilities['platformName'] == 'Android'

    def start_driver(self):
        device_id = self.desired_capabilities.get('deviceName')
        if device_id and not self.device_control.is_device_in_use(device_id):
            try:
                url = f"http://{self.server_ip[0]}:{self.server_ip[1]}/wd/hub"
                print(url)
                self.driver = webdriver.Remote(url, self.desired_capabilities)
                self.wait = WebDriverWait(self.driver, 60)
                self.device_control.set_device_status(device_id, True)
                return True,''
            except Exception as e:
                print(e)
                return False, e
        else:
            print(f"Device {device_id} is currently in use.")
            return False, "Device in use"
