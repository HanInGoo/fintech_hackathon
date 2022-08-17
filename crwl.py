import time
from selenium import webdriver
from bs4 import BeautifulSoup


def crwl_result():
    driver = webdriver.Chrome("./chromedriver")
    time.sleep(5)
    url_hf = f"https://www.hf.go.kr/hf/sub05/sub01.do?mode=list&srCategoryId1=&srSearchKey=&srSearchVal="

    driver.get(url_hf)

    element = driver.find_element("id", "search_val")
    element.send_keys("결혼")

    res = driver.page_source
    soup = BeautifulSoup(res, "html.parser")

    content_total = []
    link_total = []
    for i in range(1, 40, 1):
        path = (
            "#jwxe_main_content > div > div > div.board-list01.list-box > table > tbody > tr:nth-of-type({}) > td.title.left > a".format(
                i))
        content = soup.select(path)

        for i in content:
            content_text = i.get_text()
            content_text2 = content_text.strip()
            content_total.append(content_text2)

        for i in content:
            link = i.attrs['href']
            link_total.append("https://www.hf.go.kr/hf/sub05/sub01.do" + link)

    print(content_total)
    print(link_total)


    result = []
    for i in range(0, len(link_total), 1):
        result_1 = []
        for j in range(0, 1, 1):
            result_1.append(content_total[i])
            result_1.append(link_total[i])
        result.append(result_1)

    result_dic = {}
    for i in range(0, len(link_total), 1):
        result_dic[result[i][0]] = result[i][1]

    print(result_dic)

    return result_dic