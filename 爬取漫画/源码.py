# 导入模块
from selenium import webdriver
import time
import json
import requests
import os

# 设置浏览器选项
caps = {
    "browserName": "chrome",
    'goog:loggingPrefs': {'performance': 'ALL'}
}
options = webdriver.ChromeOptions()
for key, value in caps.items():
    options.set_capability(key, value)

# 创建WebDriver实例
driver = webdriver.Chrome(options=options)

# 访问网站
driver.get("https://www.dmzj.com/info/yaoshenji.html ")

# 点击第一个元素
element = driver.find_element('xpath','//*[@id="__nuxt"]/div/div[3]/div[1]/div[4]/div[2]/ul/li[253]/a')
element.click()
time.sleep(3)

# 点击第二个元素
a = driver.find_element('xpath','//*[@id="__nuxt"]/div/div[2]/div[4]/a[2]')
a.click()
time.sleep(3)

# 切换到新的窗口句柄
all_handles = driver.window_handles
driver.switch_to.window(all_handles[-1])

# 获取日志信息
logs = driver.get_log('performance')
# 遍历日志信息
for log in logs:
    # 把每个日志元素的消息转换成字典
    message = json.loads(log['message'])
    # 判断消息的方法是否为Network.responseReceived
    if message['method'] == 'Network.responseReceived':
        # 获取请求的网址
        url = message['params']['response']['url']
        # 判断请求的网址是否与你给的网址相同
        if url == 'https://www.dmzj.com/api/v1/comic1/chapter/detail?channel=pc&app_name=dmzj&version=1.0.0&timestamp=1689840698296&uid&comic_id=20926&chapter_id=41919':
            # 获取响应内容的编码方式
            encoding = message['params']['response']['headers']['content-encoding']
            # 获取响应内容的二进制数据
            data = message['params']['response']['body']
            # 根据编码方式解码响应内容
            if encoding == 'gzip':
                content = gzip.decompress(data).decode('utf-8')
            elif encoding == 'br':
                content = brotli.decompress(data).decode('utf-8')
            else:
                content = data.decode('utf-8')
            # 把响应内容转换成Python对象
            content = json.loads(content)
            # 提取图片url列表
            image_urls = content['data']['chapterInfo']['page_url']
            # 创建一个文件夹来保存图片
            folder = 'images'
            if not os.path.exists(folder):
                os.mkdir(folder)
            # 遍历图片url列表
            for image_url in image_urls:
                # 获取图片的名称
                image_name = image_url.split('/')[-1]
                # 拼接图片的保存路径
                image_path = os.path.join(folder, image_name)
                # 发送请求获取图片的二进制数据
                response = requests.get(image_url)
                data = response.content
                # 保存图片到本地
                with open(image_path, 'wb') as f:
                    f.write(data)
                # 打印提示信息
                print(f'已保存图片: {image_path}')

