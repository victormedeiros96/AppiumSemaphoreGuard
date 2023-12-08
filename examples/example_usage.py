from appium_driver.appium_driver_basic import AppiumDriverBasic

server_ip = "localhost"
server_port = 4723
desired_capabilities = {
    'platformName': 'Android',
    'deviceName': 'device123'
}

driver = AppiumDriverBasic(server_ip, server_port, desired_capabilities)
success, message = driver.start_driver()

if success:
    print("Driver started successfully.")
else:
    print(f"Failed to start driver: {message}")
