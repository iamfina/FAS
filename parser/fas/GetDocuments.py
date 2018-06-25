import requests
from bs4 import BeautifulSoup
import csv
import time
import json
import socks
import socket
from fake_useragent import UserAgent
from tqdm import tqdm
import pandas as pd
from multiprocessing import Pool, cpu_count
from multiprocessing.pool import ThreadPool
import sys
import random
## требуется установка tor браузера. на момент парсинга он должен быть запущен.


def Reduce(l):# объединяем списки от каждого потока
    df = pd.DataFrame( )
    frames = [ pd.DataFrame(item) for item in l ]
    df = pd.concat(frames)
    return(df) 

def GetID(part_hrefs):
    href=str(' '.join(part_hrefs.split())) #удаляем непечатные символы из ссылок
    with requests.Session() as session: # сессия для requests
        status_code=0
        while status_code != 200: # долбим запросами пока не вернется ответ 200
            try:
                r=session.get('https://solutions.fas.gov.ru'+href, headers={'User-Agent': UserAgent().random})
                #status_code =r.status_code
                status_code =200
            except Exception:
                pass
        try:
            soup = BeautifulSoup(r.text, 'html.parser') # ответ передаем в суп
            txt_label=soup.find('h1', {'class': 'page_title'}).text #заголовок документа
            txt_document=soup.find('div', {'class': 'document_description'}).text #текст документа

            #получаем из документа атрибуты документа. т.к. их разное количество и порядок, заносим их в словарь. 
            #для названия атрибута и свойства
            document_info_label= soup.find_all('div', {'class': 'document_info_label'}) # все названия атрибутов документа
            document_info_content= soup.find_all('div', {'class': 'document_info_content'}) # все значения атрибутов документа

            txt__dict={} # заполняем словарь. если 
            for val in range (0,len(document_info_label)):
                txt__dict.update({document_info_label[val].text: document_info_content[val].text})

            # запоняем переменные если они есть иначе -
            txt__doc_type=txt__dict.get('Тип документа:','-')
            txt__date_pub=txt__dict.get('Дата публикации:','-')
            txt__territory=txt__dict.get('Управление:','-')
            txt__sphere=txt__dict.get('Сфера деятельности:','-')
            txt__delo_number=txt__dict.get('Номер документа:','-')
            txt__doc_number=txt__dict.get('Номер дела:','-')


            #       для документов с вложениями ищем все  
            txt__doc_attach_=soup.find_all('div', {'class': 'document_attachment_text'})
            txt__doc_attach = (', ').join([a.find('a')['href'] for a in txt__doc_attach_]) # все ссылки, если их больше 1 объеденяем через запятую.

            # пихаем все переменные в список и передаем его обратно.
            txt__doc=[]
            txt__doc.append(href) #ссылка на документ
            txt__doc.append(txt_label) #заголовок документа
            txt__doc.append(txt__doc_type) #тип документа
            txt__doc.append(txt__date_pub) #дата публикации
            txt__doc.append(txt__territory) #управление
            txt__doc.append(txt__sphere) #сфера деятельности
            txt__doc.append(txt__delo_number) #номер документа
            txt__doc.append(txt__doc_number) #номер дела
            txt__doc.append(txt__doc_attach) #ссылки на прикрепленные документы
            txt__doc.append(txt_document) #текст документа
            time.sleep(0.5)
        except Exception:
            txt__doc=[]
            txt__doc.append(href) #ссылка на документ
            txt__doc.append("no text") #заголовок документа
            txt__doc.append("-") #тип документа
            txt__doc.append("-") #дата публикации
            txt__doc.append("-") #управление
            txt__doc.append("-") #сфера деятельности
            txt__doc.append("-") #номер документа
            txt__doc.append("-") #номер дела
            txt__doc.append("-") #ссылки на прикрепленные документы
            txt__doc.append("-") #текст документа           
            pass
        return (txt__doc)

def GetData(part_hrefs): # визуализация в рамках каждого задания на получение материала. (tqdm не пашет нормально.)
    df = []
    for item in tqdm(part_hrefs, position=2, desc="h", leave=False):
        responseDic = GetID(item) # получаем данные по конкретной ссылке
        df.append(responseDic) # добавляем в список данные.
    return(df)

def main():
    PoolCount=500 #количество потоков
    
    with open('fas/Doc_link_p2.csv', 'r') as file: # читаем файл со ссылками на страницы в список
        TotalLinks =file.readlines()
        
        #разбиаем список со ссылками пропорционально потокам
    parts = [round(len(TotalLinks)/PoolCount)*i for i in range(PoolCount)]
    parts.append(len(TotalLinks))
    names = [TotalLinks[parts[i]:parts[i+1]] for i in range(PoolCount)]
   
    # выполняем парсинг для каждого списка ссылок в рамках потока
    pool = ThreadPool(PoolCount)
    l = pool.map(GetData, names)
    
    # объединяем списки с данными в df
    itog_data=Reduce(l)
    pd.DataFrame.to_csv(itog_data,'fas/docs_t2.csv') #сохраняем df
    
    

if __name__=='__main__':
    print ("start")
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)# нужно чтобы парсить через тор. в настройках браузера стоит спена ip каждыю 10 сккундю сам браузер нужно запускать, чтобы был открыт.
    socket.socket = socks.socksocket #
    main()
    print ("finish")
