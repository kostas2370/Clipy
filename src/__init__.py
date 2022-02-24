import other
import youtube_funcs
import edit
import setup
import os
import glob
import upload
import time
import real_upload
import twitch_funcs
def video(get_clips=True,title="default",amt=20,music=False,music_selection="default",game=False,intro=True,outro=True,serie="Random Compilation",api=False):
		if (get_clips ==True): 
			
			try:	
				P=(twitch_funcs.get_clips(game_name=game,amt=amt))
				
			except:
				print("anavaliable game")
				return False
		try:
			x=edit.vidMake_mode_compilation(amt,title,music=music,music_selection=music_selection,intro=intro,outro=outro,serie=serie,game=game)
		except:
			print ("Cant")
			return False

		real_upload.upload(x[0],x[1],x[2],api)

def test():
	#setup.setup()
	#video(get_clips=True,title="Minecraft",game="Minecraft",amt=15)
	#
	#youtube_funcs.download_youtube("https://www.youtube.com/watch?v=xi0FP37j9eU")
	#youtube_funcs.download_youtube("https://www.youtube.com/watch?v=detuR2Yj7fw")
	#
	#p=other.get_Destination(0)
	#other.set_intro("C:/Users/mr_Dmn/Desktop","/intro.mp4")
	#other.set_outro("C:/Users/mr_Dmn/Desktop","/outro.mp4")
	#print(youtube_funcs.download_youtube("https://www.youtube.com/watch?v=APq4nz2mydM","mp3"))
	#print(youtube_funcs.download_youtube("https://www.youtube.com/watch?v=0MvrujXFVDs","mp3"))
	#print(youtube_funcs.download_youtube("https://www.youtube.com/watch?v=zx3Q2PGqh6I","mp3"))
	#print(youtube_funcs.download_youtube("https://www.youtube.com/watch?v=SokYPg-1kkE","mp3"))
	#video(game="Minecraft")
	#print(upload.get_video_title("Random Compilation"))
	video(game="Need for Speed Heat",amt=15,serie="Need for Speed Heat Compilation",get_clips=True)
	#print(upload.get_video_title("Random Compilation"))
	#print(twitch_funcs.get_clips(amt=20,game_name="League of Legends"))
	#twitch_funcs.get_clips(amt=5,game_name="Minecraft")
	#print(other.get_creator("FIRST DREAM SMP STREAM (ft. Dream).mp4"))
	#real_upload.upload(x[0],x[1],x[2],api=True)
	#print (upload.get_video_description())

	#print(x)
	

test()