
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import urllib.request
import other 
import sqlite3
from moviepy.editor import *
import datetime
import os
import glob
import json
import requests
import twitch
import random
def download_twitch(link="",game="",title="",creator=""):
    creator=creator
    title=title

    if (link==""):
        return("you need to put a link")

    path_save=other.get_Destination(0)

    s=Service("<selenium_path>")
    
    driver = webdriver.Chrome(service=s)
    try:
        driver.get(link)
        
    except:
        return "This link doest work"
    time.sleep(3)
    try:
        download_link=str(driver.find_element(By.TAG_NAME,"video").get_attribute("src"))
    except:
        return "This clip doesnt exist"
   
    
    if other.check_file(title)==True:
        driver.close()
        return ("this video already exists")
    else:
        if other.check_if_db(link)==True:
            driver.close()                 
            return "This video exists"  
    
        
    
    try:    
        urllib.request.urlretrieve(download_link, path_save+"/"+title+".mp4") 
        driver.close()
    except:
        driver.close()
        return "Couldn't download"
    
    x=VideoFileClip(path_save+"/"+title+".mp4")
    duration=x.duration 
    size=x.duration   
    list_of_files = glob.glob(other.get_Destination(0)+"/*.mp4")
    video_name=str(os.path.basename(max(list_of_files,key=os.path.getctime)))
    download_date=str(datetime.date.today())

    conn=sqlite3.connect("db/database.db")
    c=conn.cursor()
    c.execute("INSERT INTO youtube_clips (title,duration,video_link,download_date,avaliability,filesize,file_name,channel_name,clip_type,game) VALUES (?,?,?,?,?,?,?,?,?,?)",[title,duration,link,download_date,"downloaded",size,video_name,creator,"twitch",game])    
    conn.commit()
    conn.close()
    print (title+" downloaded succesfuly")
    return True



def get_game_ids(game_name):
    client = twitch.TwitchHelix(client_id='<client_id>', client_secret='<client_secret>', scopes=[twitch.constants.OAUTH_SCOPE_ANALYTICS_READ_EXTENSIONS])
    client.get_oauth()
    game_id=client.get_games(names=game_name)
    x=game_id[0]["id"]
    return x




def get_clips(amt=10,game_name="",streamer_id=""):
    
    succesful=0
    now=datetime.date.today()
    client = twitch.TwitchHelix(client_id='<client_id>', client_secret='<client_secret>', scopes=[twitch.constants.OAUTH_SCOPE_ANALYTICS_READ_EXTENSIONS])
    client.get_oauth()
    if game_name=="":
        print("you need to put game names")
        return False
    elif type(game_name)=="int":
        try:
            p=client.get_clips(game_id=games_name,started_at=other.get_previous_day(),page_size=100)

            
        except:
            return "not avaliable id"

    else:
        try:
            ids=get_game_ids(game_name)
            y=client.get_clips(game_id=ids,started_at=other.get_previous_day(),page_size=100)
            print(len(y))
            x=other.check_lang(y)

        except:
            return "not avaliable id"
         
   
    for i in range(len(x)):
        
        if succesful!=amt:
            br=download_twitch(link=x[i]["url"],game=game_name,creator=x[i]["creator_name"],title=x[i]["title"])
            if(br==True):
                succesful=succesful+1
           
        else:
            break

    return succesful        





