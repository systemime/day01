import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq
import time, random
from bs4 import BeautifulSoup
# https://pyppeteer.github.io/pyppeteer/reference.html?highlight=launch#pyppeteer.launcher.launch


USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]
# # /home/workon/.local/share/pyppeteer/local-chromium/588429
# # /Users/qifeng/Library/Caches/JetBrains/PyCharm2020.1/remote_sources/470328456/-236235940/pyppeteer/chromium_downloader.py
#
# # import pyppeteer.chromium_downloader
# # # 这里的 linux 替换成你系统的版本，win32，win64，linux
# # # 这个是返回在当前系统下chromium的路径
# # print(pyppeteer.chromium_downloader.chromiumExecutable.get("linux"))
# # # 这个是返回当前系统默认的下载地址
# # print(pyppeteer.chromium_downloader.downloadURLs.get("linux"))
#
#
# async def main():
#     browser = await launch()
#     page = await browser.newPage()
#     await page.goto('https://www.baidu.com/')
#     doc = pq(await page.content())
#     print('Quotes:', doc('.quote').length)
#     await browser.close()
#
#
# asyncio.get_event_loop().run_until_complete(main())


# 关闭当前打开的浏览器中的一个界面；--OK--
async def closePage(page):
    await page.close()


# 滚动到页面底部 --OK--
async def scrollToButtom(page):
    await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
    print("滑动到当前界面底部【完毕】")


async def find_iframe(browser, page):
    try:
        await asyncio.sleep(1)

        frame = page.frames
        print(frame)  # 需要找到是哪一个 frame
        title = await frame[1].title()
        print(title)
        await asyncio.sleep(1)
        login = await frame[1].querySelector('#switcher_plogin')
        print(login)
        await login.click()

        await asyncio.sleep(20)
    except Exception as e:
        print(e, "EEEEEEEEE")

    for _page in await browser.pages():
        await _page.close()


async def main():

    js1 = '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }'''

    js2 = '''() => {
            alert (
                window.navigator.webdriver
            )
        }'''
    js3 = '''() => {
            window.navigator.chrome = {
        runtime: {},
        // etc.
      };
        }'''

    js4 = '''() =>{
    Object.defineProperty(navigator, 'languages', {
          get: () => ['en-US', 'en']
        });
            }'''

    js5 = '''() =>{
    Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5,6],
      });
            }'''

    # browser = await launch(userDataDir='./userdata', args=['--disable-infobars'])
    browser = await launch(
        args=['--no-sandbox']
    )
    page = await browser.newPage()

    # 设置请求头header信息
    await page.setExtraHTTPHeaders({
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
    })
    # 为False忽略js渲染
    await page.setJavaScriptEnabled(enabled=True)
    await page.goto('https://blog.csdn.net/m0_46521476/article/details/107903174', options={'timeout': 1000})
    await page.evaluate(js1, js3, js4, js5)
    # 刷新后页面webdriver属性不变
    await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                     '{ webdriver:{ get: () => false } }) }')
    # # 截图
    # await page.evaluate(js2)
    # await page.screenshot({'path': 'example.png'})

    # 获取页面title
    title = await page.title()
    print("页面标题为：", title)

    # 获取主体
    doc = await page.content()  # 获取html
    # with open("index.html", "w+") as f:
    #     f.write(doc)

    # 抓取新闻内容  可以使用 xpath 表达式
    """
    # Pyppeteer 三种解析方式
    Page.querySelector()  # 选择器
    Page.querySelectorAll()
    Page.xpath()  # xpath  表达式
    # 简写方式为：
    Page.J(), Page.JJ(), and Page.Jx()
    """
    element = await page.querySelector(".feed-infinite-wrapper > ul>li")  # 纸抓取一个
    print(element)
    # 获取所有文本内容  执行 js
    content = await page.evaluate('(element) => element.textContent', element)
    print(content)

    # elements = await page.xpath('//div[@class="title-box"]/a')
    elements = await page.querySelectorAll(".title-box a")
    for item in elements:
        print(await item.getProperty('textContent'))
        # <pyppeteer.execution_context.JSHandle object at 0x000002220E7FE518>

        # 获取文本
        title_str = await (await item.getProperty('textContent')).jsonValue()

        # 获取链接
        title_link = await (await item.getProperty('href')).jsonValue()
        print(title_str)
        print(title_link)

    """
    今日头条：抓取范例
    # 抓取新闻标题
    title_elements = await page.xpath('//div[@class="title-box"]/a')
    for item in title_elements:
        # 获取文本
        title_str = await (await item.getProperty('textContent')).jsonValue()
        print(await item.getProperty('textContent'))
        # 获取链接
        title_link = await (await item.getProperty('href')).jsonValue()
        print(title_str)
        print(title_link)
    """

    titles = BeautifulSoup(doc, 'lxml').find_all('div')
    print("页面主体为：")
    for i in titles:
        print(i.find('p'))

    # 内容长度
    doc = pq(doc)
    print('Quotes:', doc('.quote').length)

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

# import os
# import time
# import json
# from urllib.parse import urlsplit
# import asyncio
# import pyppeteer
# import scripts
#
# BASE_DIR = os.path.dirname(__file__)
#
#
# async def intercept_request(req):
#     """请求过滤"""
#     if req.resourceType in ['image', 'media', 'eventsource', 'websocket']:
#         await req.abort()
#     else:
#         await req.continue_()
#
#
# async def intercept_response(res):
#     resourceType = res.request.resourceType
#     if resourceType in ['xhr', 'fetch']:
#         resp = await res.text()
#
#         url = res.url
#         tokens = urlsplit(url)
#
#         folder = BASE_DIR + '/' + 'data/' + tokens.netloc + tokens.path + "/"
#         if not os.path.exists(folder):
#             os.makedirs(folder, exist_ok=True)
#         filename = os.path.join(folder, str(int(time.time())) + '.json')
#         with open(filename, 'w', encoding='utf-8') as f:
#             f.write(resp)
#
#
# async def main():
#     browser = await pyppeteer.launch({
#         # 'headless': False,
#         # 'devtools': True
#         # 'executablePath': '/Users/changjiang/apps/Chromium.app/Contents/MacOS/Chromium',
#         'args': [
#             '--disable-extensions',
#             '--hide-scrollbars',
#             '--disable-bundled-ppapi-flash',
#             '--mute-audio',
#             '--no-sandbox',
#             '--disable-setuid-sandbox',
#             '--disable-gpu',
#         ],
#         'dumpio': False,
#     })
#     page = await browser.newPage()
#
#     await page.setRequestInterception(True)
#     page.on('request', intercept_request)
#     page.on('response', intercept_response)
#
#     await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
#                             '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')
#     await page.setViewport({'width': 1080, 'height': 960})
#     await page.goto('http://yangkeduo.com')
#     await page.evaluate("""
#             () =>{
#                    Object.defineProperties(navigator,{
#                      webdriver:{
#                        get: () => false
#                      }
#                    })
#             }
#         """)
#     await page.evaluate("你的那一段页面自动下拉 js 脚本")
#     await browser.close()
#
#
# if __name__ == '__main__':
#     asyncio.run(main())

