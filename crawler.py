from selenium import webdriver
import time
from lxml import etree
import pandas as pd
chrome_driver='/anaconda3/pkgs/python-3.7.0-hc167b69_0/lib/python3.7/site-packages/chromedriver'
driver=webdriver.Chrome(chrome_driver) #获得Chrome driver

director='徐峥'
base_url='https://movie.douban.com/subject_search?search_text='+director+'&cat=1002&start='

movie_actor = {}
def get_data(url):
    driver.get(url)
    time.sleep(1)
    html = driver.find_element_by_xpath("//*").get_attribute("outerHTML") #获得页面的整个文档
    html=etree.HTML(html) #获得所有单个元素
    movies=html.xpath("/html/body/div[@id='wrapper']/div[@id='root']/div[1]//div[@class='item-root']/div[@class='detail']/div[@class='title']/a[@class='title-text']")
    #movie_lists = html.xpath("/html/body/div[@id='wrapper']/div[@id='root']/div[1]//div[@class='item-root']/div[@class='detail']/div[@class='title']/a[@class='title-text']")
    actors=html.xpath("/html/body/div[@id='wrapper']/div[@id='root']/div[1]//div[@class='item-root']/div[@class='detail']//div[@class='meta abstract_2']")
    num=len(movies)
    if num>15:
        movies=movies[1:]
        actors=actors[1:]
    for (movie,actor) in zip(movies,actors):
        if actor.text is None:
            continue
        movie_actor[movie.text]=actor.text.replace(' ','')
    if num>15:
        return True
    else:
        return False


start=0

while start<10000:
    url=base_url+str(start)
    flag=get_data(url)
    if flag:
        start=start+15
    else:
        break

movie_actor_df=pd.DataFrame.from_dict(movie_actor,orient='index',columns=['actors'])
movie_actor_df=movie_actor_df.reset_index().rename(columns={'index':'name'})
movie_actor_df.to_csv('movie.csv')

data=pd.read_csv('movie.csv')
print(data.iloc[:,1:])



