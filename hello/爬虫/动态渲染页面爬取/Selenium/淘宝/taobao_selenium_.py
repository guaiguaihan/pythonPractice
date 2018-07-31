from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Chrome

from urllib.parse import quote

from config import *

# 无界面浏览
# 已经不支持了
# browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = Chrome(chrome_options=chrome_options)


wait = WebDriverWait(browser, 15)


def index_page(page):
    """
    抓取索引页
    :type page: 页码
    """
    print('开始爬取第 ', page, '页')
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEY_WORD)
        browser.get(url=url)
        print(url)
        if page > 1:
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit'))
            )
            print('开始提交请求')
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page))
        )
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item'))
        )
        get_products()
    except TimeoutException:
        index_page(page=page)


from pyquery import PyQuery as pq


def get_products():
    """
    提取商品数据
    :return:
    """
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)


from pymongo import MongoClient

client = MongoClient(MONGO_URL)
db = client[MONGO_DB]


def save_to_mongo(product):
    """
    保存到数据库
    :param product:
    :return:
    """
    try:
        if db[MONGO_COLLECTION].insert(product):
            print('插入数据', product.get('title'), '成功')
    except Exception:
        print('插入数据', product.get('title'), '失败')


def main():
    """
    遍历 100
    :return:
    """
    for i in range(1, MAX_PAGE + 1):
        index_page(i)


if __name__ == '__main__':
    main()