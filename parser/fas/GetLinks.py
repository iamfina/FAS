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



def Reduce(l):
    df = pd.DataFrame( )
    frames = [ pd.DataFrame(item) for item in l ]
    df = pd.concat(frames)
    return(df)  

def GetID(part_hrefs):
    #proxies_=get_proxy()
    with requests.Session() as session:
        status_code=0
        while status_code != 200:
            try:
                r=session.get("https://solutions.fas.gov.ru/?page="+str(part_hrefs), headers={'User-Agent': UserAgent().random})
                status_code =r.status_code
            except Exception:
                #proxies_=get_proxy()
                pass
    soup = BeautifulSoup(r.text, 'html.parser').find('div', {'class': 'documents_list'})
    links_with_text = [a['href'] for a in soup.find_all('a', href=True) if a.text]
    return (links_with_text)




def GetData(part_hrefs):
    df = []
    for item in tqdm(part_hrefs, position=2, desc="h", leave=False):
        responseDic = GetID(item)
        df+=responseDic
    return(df)
 



def main():
    PoolCount=100
    TotalLinks=44588
    TotalLinksList=[iz for iz in range(1,TotalLinks+1,1)]
    parts = [round(len(TotalLinksList)/PoolCount)*i for i in range(PoolCount)]
    parts.append(len(TotalLinksList))
    names = [TotalLinksList[parts[i]:parts[i+1]] for i in range(PoolCount)]
    
    pool = ThreadPool(PoolCount)
    l = pool.map(GetData, names)
   

    itog_data=Reduce(l)
    pd.DataFrame.to_csv(itog_data,'fas/_test_0.csv')


if __name__=='__main__':
    print ("start")
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
    socket.socket = socks.socksocket
    main()
    print ("finish")
