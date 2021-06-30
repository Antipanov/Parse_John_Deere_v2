from selenium import webdriver
import requests
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import chromedriver_binary
import urllib
import os
from os import rename, listdir
import csv


# эта функция сохраняет картинку в папку
def save_my_pictures(link):
    filename = link.split('/')[-1]
    print(filename)
    r = requests.get(link, allow_redirects=True)
    open(filename, "wb").write(r.content)
    print("скохранил")


# Мы уехали с официального сайта на technodom, т.к. структура оффициальном стуктура гадость
# Сейчас мы разберёмся с тракторами и на основе этого скрипта завигачу скрипт для всего остального


#######################################################################################################################################################################################################################################
def parse_info():
    try:
        info_about_technics1 = driver.find_elements_by_xpath("//div[@class='col-12']//p")[0]
        info_about_technics2 = driver.find_elements_by_xpath("//div[@class='col-12']//p")[5]
        info_about_technics3 = driver.find_elements_by_xpath("//div[@class='col-12']//p")[9]
        info_about_technics = info_about_technics1.text + info_about_technics2.text + info_about_technics3.text
    except:
        info_about_technics = driver.find_element_by_xpath("//div[@class='tab_pr_description active tabs__content']//p").text
    print(info_about_technics)
    url_page_tractor_info = driver.current_url
    print(url_page_tractor_info)
    # нахожу картинку в карточке товара
    info_about_technics = info_about_technics.replace(',', '')
    name_of_picture = names + ".jpg"
    name_of_picture = name_of_picture.replace(' ', '_')
    brand_name = "John Deere"
    group = "Сельскохозяйственная техника"
    result_row = [group, brand_name, type_of_tech, names, info_about_technics, url_page_tractor_info, name_of_picture]
    csv_writer.writerow(result_row)
    print("")


def parse_img():
    try:
        find_element = driver.find_elements_by_xpath("//a[@class='productimage']//img")[i]
        url_img = find_element.get_attribute("src")
        print(url_img)
        # Теперь сохраняет фото
        save_my_pictures(url_img)
        # Собираем название для картинки из названия техники и
        name_of_picture = names + ".jpg"
        name_of_picture = name_of_picture.replace(' ', '_')
        print(name_of_picture)
        # Я кладу в link ссылку на картинку, чтоб в filename питон её преобразовал в название файл который уже в папке проэкта под идиотским названием для идиотов от идиотов. Вполне логично, в духе этого кода.
        link = url_img
        # print(link)
        # filename это переменная в которую я кладу название файла которрое нужно заменить на что-то вменяемое например на название техники.
        filename = link.split('/')[-1]
        # print(filename)
        os.rename(filename, name_of_picture)
    except Exception as e:
        print(e)


# эти три строчки запускают сайт John Deere на страничке с выбором типа техники
driver = webdriver.Chrome()
url = "https://www.technodom.com/catalog/agricultural-john-deere/"
specifications_url = "https://specs.lectura.ru/ru"
driver.get(url)


urls = ["",
        "https://www.technodom.com/product/traktor-8rx-410/",
        "https://www.technodom.com/product/zhatka-rd40f/",
        "https://www.technodom.com/product/kormouborochnyj-kombajn-8500/",
        "https://www.technodom.com/product/samohodnyj-opryskivatel-m4040/",
        "https://www.technodom.com/product/pnevmaticheska-seyalka-1895/",
        "https://www.technodom.com/product/diskovaya-borona-2625/",
        "https://www.technodom.com/product/rulonnyj-press-podborshhik-f450e/",
        "https://www.technodom.com/product/gator-krossover-xuv835m/",
        "https://www.technodom.com/product/priczepnaya-kosilka-plyushhilka-s-czentralnym-krepleniem-dyshla-835/",
        "https://www.technodom.com/product/rotornaya-zhatka-994/",
        "https://www.technodom.com/product/samohodnyj-razbrasyvatel-suhih-udobrenij-dn456/"]


# ищу кнопку тракторы
with open('parse_result_v2.csv', 'w', encoding='utf8') as writefile:
    csv_writer = csv.writer(writefile, lineterminator='\r\n', quotechar="'")
    for j in range(8):
        if j != 0:
            time.sleep(2)
            type_of_tech = driver.find_elements_by_xpath("//span[@class='imcatname']")[j]
            type_of_tech = type_of_tech.text
            link_to_tech = driver.find_elements_by_xpath("//li[@class='mainitem']//a[@class='c_menua']")[j]
            link_to_tech.click()
            # Здесь я считаю количество элементов, которые нужно спарсить
            number = len(driver.find_elements_by_xpath("//div[@class='product_title']"))
            #######################################################################################################################################################################################################################################
            for i in range(number):
                time.sleep(2)
                # собираю названия тракторов
                names_of_tractors = driver.find_elements_by_xpath("//div[@class='product_title']")[i]
                names = names_of_tractors.text
                print(names, "| порядковый номер:", i + 1)
                parse_img()
                # ищу кнопку узнать больше
                if i != 1:
                    more_info = driver.find_elements_by_xpath("//a[@class='productimage']")[i]
                    try:
                        # Захожу в карточку товара
                        more_info.click()
                        # вызываю функцию для парсинга карточки товара
                        parse_info()
                    except Exception as e:
                        print(e)
                else:
                    try:
                        # Кнопка "Больше информации" на второй карточке не работает. Поэтому захожу туда через url.
                        url = urls[j]
                        print(url)
                        print(j)
                        driver.get(url)
                        parse_info()
                    except Exception as e:
                        print(e)
                driver.back()
        else:
            continue
        back_to_groups = "https://www.technodom.com/catalog/agricultural-john-deere/"
        driver.get(back_to_groups)


# закрываю браузер
driver.close()