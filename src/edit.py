import other
import youtube_funcs 
import os 
from moviepy.editor import *
import sqlite3
import random
import upload
import time
import psutil
def cut_video(video_name,start_time,end_time,clip_names="default"):
    if(len(start_time)!=len(end_time)):
        print("You forgot a time !")
        return False

    conn=sqlite3.connect("db/database.db")
    c=conn.cursor()
    c.execute("SELECT  clips_to_delete_destination FROM settings")
    for row in c.fetchall():
        destination=row[0]
   
    try:
        path=other.get_Destination(0)
        vid=path+"/"+video_name
        for x in range(len(start_time)):
                st=start_time[x]
                et=end_time[x]
                clip=VideoFileClip(vid,fps=30)
                if(clip.duration<st or clip.duration<et):
                        print(str(x)+"clip above limit")
                else:
                        clip=clip.subclip(st,et)
                        if clip_names=="default":
                            filename=video_name+" clip "+str(x)+".mp4"
                        else:
                            filename=clip_names[x]+".mp4"
               
                        c.execute("SELECT channel_name,video_link FROM youtube_clips WHERE file_name = '{}'".format(video_name))
                        for row in c.fetchall():
                            channel_name=row[0]
                            video_link=row[1]   
                        c.execute("INSERT INTO cutted_clip(clip_name,full_video_name,publisher,link,time_START,time_END) VALUES(?,?,?,?,?,?)",[filename[0:len(filename)-3],video_name,channel_name,video_link,start_time[x],end_time[x]])
        
                        print(filename)
                        clip.write_videofile(path+"/"+filename)  
                        clip.close()

        other.move_file(vid,destination+"/"+video_name) 
     
        conn.commit()
        conn.close()
    except:
        print("couldnt find the file name D: ") 
        return  False

def convert_to_mp3(video_name,after=True):
    
    destination_of_video=other.get_Destination(0)
    destination_of_save=other.get_Destination(3)
    try:
        vid=VideoFileClip(destination_of_video+"/"+video_name+".mp4")
        vid.audio.write_audiofile(destination_of_save+"/"+video_name+".mp3")
        vid.close()
    except:
         print("Cant find this video !")  
         
         return False

    print("Success")  
    if(after==True):
        other.move_file(other.get_Destination(0)+"/"+video_name+".mp4",other.get_Destination(2)+"/"+video_name+".mp4")




    return True

def vidMake_mode_compilation(amt,title,music=False,music_selection="default",intro=False,outro=False,serie="Random stream compilation",game=False):
           
    x=other.get_video_files(game=game)
    if (amt>len(x)):
        amt=len(x)
    vidList=other.snuffle(x,amt=amt)
    video=[]
    m=other.get_Destination(0)
    conn=sqlite3.connect("db/database.db")
    c=conn.cursor()

    for x in  vidList:
        print(x)
        
        try:
            clip=VideoFileClip(m+"/"+x)
        except:
            vidList.remove(x)
            continue

        dur=str(int(clip.duration)-2)
        text=x[0:len(x)-3]
        try:
            text2=other.get_creator(x)
        except:
            text2=""     
        d=m+"/"+(x)
        save=(other.get_Destination(0)+'/edited/'+x)
        if clip.w !=1920 or clip.h !=1080:
            args1=f"ffmpeg -i \"{d}\" -vf \"scale=1920:1080,drawtext=text='{text}':x=960:y=1030:fontsize=44:fontcolor=white,drawtext=text='{text2}':x=960:y=50:fontsize=44:fontcolor=white,fade=t=in:st=0:d=2,fade=t=out:st={dur}:d=2\" \"{save}\""
        else:
            args1=f"ffmpeg -i \"{d}\" -vf \"drawtext=text='{text}':x=960:y=1030:fontsize=44:fontcolor=white,drawtext=text='{text2}':x=960:y=50:fontsize=44:fontcolor=white,fade=t=in:st=0:d=2,fade=t=out:st={dur}:d=2\" \"{save}\""
        os.system(args1)   
       
        time.sleep(1)
        
        
    parent = psutil.Process()    
    for child in parent.children(recursive=True): 
            try:
                if (child.name()=="ffmpeg-win64-v4.2.2.exe"):
                
                    child.kill()
            except:
                print("Child got killed")
    for b in vidList:
            
        other.move_file(m+"/edited/"+b,m+"/"+b)
    for x in vidList:
        try:
            clip=VideoFileClip(m+"/"+x) 
            video.append(clip)
        except:
            os.remove(other.get_Destination(0)+"/"+x)
            vidList.remove(x)
            print("not this vid")

    final_video=concatenate_videoclips(video)            
    if (music==True):
        musicf=select_song()
        musicx=AudioFileClip(musicf).volumex(0.15)
        print("music")
        if musicx.duration>final_video.duration:
            final_audio=CompositeAudioClip([final_video.audio,musicx]).subclip(0,final_video.duration)
        else:
            final_audio=CompositeAudioClip([final_video.audio,musicx])
        final_video=final_video.set_audio(final_audio)
    
   



    p=other.get_Destination(1)
    if (os.path.exists(other.get_Destination(4)+"/"+"intro.mp4") and intro==True):
        try:
            introcl=VideoFileClip(other.get_Destination(4)+"/"+"intro.mp4")
            print (introcl.duration)
        except:
            print("You haven't set intro !")
            intro=False
    else: 
        intro=False
    if (os.path.exists(other.get_Destination(4)+"/"+"outro.mp4") and outro==True ):
        try:
            outrocl=VideoFileClip(other.get_Destination(4)+"/"+"outro.mp4")
            print (outrocl.duration)
        except:
            print("You haven't set intro !")       
    else: 
        outro=False
    

    if (intro and outro):
        print("intro and outro")
        
        final_video2=concatenate_videoclips([introcl,final_video,outrocl])      
        final_video2.write_videofile(p+"/"+title+".mp4",threads = 8,fps=30)
        final_video2.close()
    elif(intro and outro==False):
        print("intro")
        final_video2=concatenate_videoclips([introcl,final_video],method='compose')
        final_video2.write_videofile(p+"/"+title+".mp4",threads = 8,fps=30)
        final_video2.close()
    elif(intro==False and outro):
        print("outro")
        final_video2=concatenate_videoclips([final_video,outrocl2],method='compose')
        

        final_video2.write_videofile(p+"/"+title+".mp4",threads = 8,fps=30)
        final_video2.close()
    else:
        
        final_video.write_videofile(p+"/"+title+".mp4",threads = 8,fps=30)
        final_video.close()
    



    conn=sqlite3.connect("db/database.db")
    c=conn.cursor()
    
    titles=upload.get_video_title(serie)
    
    if music==False :
        description=upload.get_video_description(vidList)
    else:
        description=upload.get_video_description(vidList,musicf)
    try:
        os.rename(p+"/"+title+".mp4",p+"/"+titles+".mp4")  
    except:
        if os.path.exists(p+"/"+title+".mp4",p+"/"+titles+".mp4"):
            os.rename(p+"/"+title+".mp4",p+"/"+"default.mp4")
    file_name=p+"/"+titles+".mp4"
    c.execute("INSERT INTO videos(video_name,serie,description,filename_path) VALUES (?,?,?,?)",[titles,serie,description,file_name])
    conn.commit()
    conn.close()
    for x in video:
        x.close()
    for x in vidList:
        try: 
            other.move_file(m+"/"+x,other.get_Destination(2)+"/"+x)
        except:
            print ("Cant move a file !")    
    return [titles,description,file_name]
    
def select_song(music_selection="default"):
        
        music_folder=other.get_Destination(3)
        if (music_selection=="default"):
            p=os.listdir(music_folder)
            song_choice=random.randint(0,len(p)-1)
            song=p[song_choice]
        else:
            if os.path.exists(music_folder+"/"+music_selection):
                song=music_selection+".mp3"
            else:
                print("I can't find this song")
                return 0
        music=music_folder+"/"+song
        

        return music

"""
for x in vidList:
        
        clip=VideoFileClip(m+"/"+x)    
        text=x[0:len(x)-3]
        text2=other.get_creator(x)
        textclp=TextClip(text, fontsize = 35, color = 'white',font="The Sirens")
        textclp=textclp.set_pos("top").set_duration(clip.duration)
        creator=TextClip(text2, fontsize = 35, color = 'white',font="The Sirens")
        creator=creator.set_pos("bottom").set_duration(clip.duration)
        fnl_clip=CompositeVideoClip([clip,textclp])
        fnl_clip2=CompositeVideoClip([fnl_clip,creator])
        video.append(fnl_clip2)

    slided_clips1 = [CompositeVideoClip([clip.fx( transfx.fadein,  1)]) for clip in video]

    slided_clips2 = [CompositeVideoClip([clip.fx( transfx.fadeout, 1)]) for clip in slided_clips1]
    final_video=
    print("bruh")
"""