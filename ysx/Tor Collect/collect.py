import subprocess
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import os

# 配置 Tshark 以捕获 Tor 浏览器的流量数据
def start_tshark_capture(output_file="tor_capture.pcapng", interface="lo0"):
    tshark_cmd = [
        "tshark",
        "-i", interface,  # Network interface
        "-Y", "tcp.port==9150 || tcp.port==9050",  # Tor SOCKS Proxy ports
        "-w", output_file  # Output file
    ]
    return subprocess.Popen(tshark_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 配置 Tor 代理
TOR_PROXY = "127.0.0.1:9050"

# 配置 Firefox 选项
options = Options()
options.headless = False  # 如果需要无头浏览器，将其设置为 True
options.set_preference("network.proxy.type", 1)
options.set_preference("network.proxy.socks", "127.0.0.1")
options.set_preference("network.proxy.socks_port", 9050)
options.set_preference("network.proxy.socks_remote_dns", True)

# 指定 Tor 浏览器的路径
firefox_binary_path = '/path/to/tor-browser/Browser/firefox'
options.binary_location = firefox_binary_path

# 启动 Tshark 捕获流量
tshark_proc = start_tshark_capture(output_file="tor_capture.pcapng", interface="lo0")

# 启动 Tor 浏览器
driver = webdriver.Firefox(options=options)

# 测试 IP 地址
driver.get("https://check.torproject.org/")
time.sleep(5)

# 查找确认文本以确保代理设置正确
element = driver.find_element(By.TAG_NAME, "h1")
if "Congratulations" in element.text:
    print("Tor is working correctly")
else:
    print("Tor is not working")

# 抓取目标网页数据
driver.get("https://example.com")
time.sleep(5)

# 关闭浏览器
driver.quit()

# 停止 Tshark 捕获
tshark_proc.terminate()
tshark_proc.wait()

print("Traffic capture completed. Saved as 'tor_capture.pcapng'.")
