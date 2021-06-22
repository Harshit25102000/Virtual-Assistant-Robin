"""Author - Harshit Singh
Published on 12 April 2021
Version 2.5 """


import threading
import selenium
from sys import exit
from time import sleep
from selenium import common
from selenium.webdriver import Chrome;
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options;
from selenium.webdriver.support import expected_conditions as EC;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support.ui import WebDriverWait;         #music imports
import requests
import json
import urllib.parse
import pyttsx3  #offline text to speech conversion library
import datetime
import time
import speech_recognition as sr   #speech recog library
import wikipedia
import smtplib
import webbrowser
from joke.jokes import *
from joke.quotes import *
from random import choice
from ytmusicapi import YTMusic
ytmusic = YTMusic()
import os
webbrowser.register('chrome',None, webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe")) #setting chrome as default browser else internet explorer will be used as default
webbrowser = webbrowser.get('chrome')  #this will open chrome if not opened or create a new tab


engine = pyttsx3.init('sapi5')  #sapi5 is ms speaking API
voices = engine.getProperty('voices')
#print(voices[1].id)  voice at 1 id is zira i.e female and 0 is david
engine.setProperty('voice', voices[1].id)  #setting zira voice


def speak(audio):  #creating speaking function
    engine.say(audio)
    engine.runAndWait() #without you won't be able to listen

def wishMe(): #function to wish
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <12:
        speak("Good Morning")
    elif hour >= 12 and hour <18:
        speak("Good Afternoon")
    else :
        speak("Good Evening")
    speak("I am Robin, how may I help you")


def jokes():
    # This will import all joke-functions (geek, icanhazdad, chucknorris, icndb)
    # Now you can use them to get some jokes.
    # Or get a random joke-function.

    j = (choice([geek, icanhazdad, chucknorris, icndb])())
    print(j)
    speak(f"ok listen to this one {j}")


def quotes():
    a = (quotesondesign())
    b = (choice(a))
    print(b[3:])
    speak(f"ok listen to this quote{b[3:]}")

def weather(key):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={key}&appid=f2718626b1ab6b8918a9db7bb655a958"
        news = requests.get(url).text
        x = json.loads(news)



        if x["cod"] != "404":

            # store the value of "main"
            # key in variable y
            y = x["main"]

            # store the value corresponding
            # to the "temp" key of y
            current_temperature = y["temp"]

            # store the value corresponding
            # to the "pressure" key of y
            current_pressure = y["pressure"]

            # store the value corresponding
            # to the "humidity" key of y
            current_humidiy = y["humidity"]
            mintemp = y["temp_min"]
            maxtemp = y["temp_max"]




            # store the value of "weather"
            # key in variable z
            z = x["weather"]

            # store the value corresponding
            # to the "description" key at
            # the 0th index of z
            weather_description = z[0]["description"]


        # print following values
            speak("ok here are weather conditions of your place ")
            print(" Temperature (in kelvin unit) = " +
                            str(current_temperature) +
                  "\n atmospheric pressure (in hPa unit) = " +
                            str(current_pressure) +
                  "\n humidity (in percentage) = " +
                            str(current_humidiy) +
                  "\n description = " +
                            str(weather_description) +
                  "\n minimum temperature (in kelvin unit) = "+
                            str(mintemp)+
                  "\n maximum temperature (in kelvin unit) =" +
                            str(maxtemp))
    except Exception as w:
        print(w)
        speak("I am sorry I can't do that right now")

def national_news():
    try:                       #national news headlines only from times of india
        speak("News for today.. Lets begin")
        url = "https://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=aff915ce85ae4475ac01ff6df1bfed46"
        news = requests.get(url).text
        news_dict = json.loads(news)
        arts = news_dict['articles']
        for article in arts:
            speak(article['title'])
            print(article['title'])
            speak("Moving on to the next news...")

        speak("Thanks for listening...")
    except Exception as n1:
        print(n1)
        speak("Sorry I am not able to read news right now")

def specific_news(keyword):  #specific_news by popularity from various sources about a specific keyword
    try:
        date = time.strftime("%y-%m-%d")
        speak("Here are top headlines ")
        url = f"https://newsapi.org/v2/everything?sources=the-times-of-india&q={keyword}&from=20{date}&sortBy=popularity&apiKey=aff915ce85ae4475ac01ff6df1bfed46"
        news = requests.get(url).text
        news_dict = json.loads(news)
        arts = news_dict['articles']
        for article in arts:
            speak(article['title'])
            print(article['title'])
            speak("Moving on to the next news...")

        speak("Thanks for listening...")
    except Exception as n2:
        print(n2)
        speak("Sorry I am not able to read news right now")

def play_music():
    class YoutubeMusic(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self);
            self.FirstTime = True;
            self.existingProj = False;
            self.IncreaseTime = 30;
            self.DecreaseTime = 30;
            self.user_agent = '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'
            self.options = Options();
            self.CompletelyLoaded = True;
            self.options.add_argument(self.user_agent);
            self.options.add_argument('--headless');
            self.options.add_argument('--disable-extensions')
            self.options.add_argument('--log-level=3')
            self.chromedriverPath = r"chromedriver.exe"; # change this with your actual chromedriver path.
            self.Browser = Chrome(self.chromedriverPath,options=self.options);
            #our browser is read to shoot.
        def HelpMenu(self):

            self.FirstTime = False

        def NavigateYoutube(self,MusicName):
            #!t Will Navigate On Youtube Website.
            self.MusicName = MusicName;
            self.CompletelyLoaded = False
            print("[Loading %s On Youtube . . . ]"%self.MusicName);
            self.Browser.get("https://m.youtube.com/results?search_query=%s"%self.MusicName);
            self.Browser.implicitly_wait(5);
        def ListVideos(self):
            self.existingProj = True;
            self.Counter = 1;
            self.Videos = [];
            for eachVid in range(1,7):
                self.xpath = '//*[@id="app"]/div[1]/ytm-search/ytm-section-list-renderer/lazy-list/ytm-item-section-renderer/lazy-list/ytm-compact-video-renderer[%d]/div/div/a/h4'%eachVid;
                self.EachVideo = WebDriverWait(self.Browser,5).until(EC.presence_of_element_located((By.XPATH,self.xpath)))
                self.EachVideo=self.EachVideo.text;
                #self.EachVideo = self.Browser.find_element_by_xpath('/html/body/ytm-app/div[3]/ytm-search/ytm-section-list-renderer/lazy-list/ytm-item-section-renderer/lazy-list/ytm-compact-video-renderer[%d]/div/div/a/h4/span'%eachVid).text;
                self.Videos.append(self.EachVideo);
            for eachVid in self.Videos:
                print("[%d]: %s"%(self.Counter,eachVid));
                self.Counter += 1;
        def RefreshPage(self):
            #!In Case Of Error Refresh Can Be Done.
            self.CurrentPage = self.Browser.current_url;
            self.Browser.get(self.CurrentPage);
            print("Page Refreshed.")
        def PlayVideo(self,VideoID):
            #Finally Plays Video.
            #!VIDEO PLAY CODE HERE
            self.VideoPlay = '//*[@id="app"]/div[1]/ytm-search/ytm-section-list-renderer/lazy-list/ytm-item-section-renderer/lazy-list/ytm-compact-video-renderer[%d]/div/div/a/h4'%VideoID;
            self.Video = WebDriverWait(self.Browser,5).until(EC.presence_of_element_located((By.XPATH,self.VideoPlay)));
            sleep(2)
            self.Video.click()

            self.VideoTitle = WebDriverWait(self.Browser,5).until(EC.presence_of_element_located((By.CLASS_NAME,'slim-video-metadata-title')));
            #self.VideoTitle = self.Browser.find_element_by_class_name('slim-video-metadata-title'); #!To Fetch Video Title.
            self.VideoTitle = self.VideoTitle.text;
            print('[Playing %s Youtube Now... ]'%self.VideoTitle);
            self.CompletelyLoaded = True;
            self.RefreshPage();
            self.GetUrl = self.Browser.find_element_by_css_selector('video.video-stream.html5-main-video');
            #self.GetUrl = WebDriverWait(self.Browser,30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'video.video-stream.html5-main-video')));
            self.GetUrl = self.GetUrl.get_attribute("currentSrc");
            self.Browser.get(self.GetUrl)
        def MoveForward(self):
            #!Time In Seconds. [ Default 30 Sec ]
            self.Browser.execute_script("document.getElementsByTagName('video')[0].currentTime += %s"%self.IncreaseTime)
        def MoveBackwards(self):
            #!Time In Seconds. [ Default : 30 Sec]
            self.Browser.execute_script("document.getElementsByTagName('video')[0].currentTime += %s"%self.DecreaseTime)
        def RestartVideo(self):
            #!Restart Current Video.
            self.CurrentVideoUrl = self.GetUrl;
            self.Browser.get(self.CurrentVideoUrl);
            pass
        def Pause(self):
            self.Browser.execute_script("document.getElementsByTagName('video')[0].pause()");
            pass
        def Play(self):
            self.Browser.execute_script("document.getElementsByTagName('video')[0].play()");
            pass
        def Close(self):
            self.Browser.close();
            exit(1)
        def ThreadStatus(self):
            print(threading.enumerate())


    x = YoutubeMusic();
    while True:

    	if x.FirstTime:
    		x.HelpMenu();
    	else:
    		try:
    			if x.existingProj == True:
    				# if project is already running.
    				
    				contentchoice = int(input("[ Song Number / 98 For CMD / Press 99 For Backward ] : "))
    				if contentchoice == 0:
    					x.PlayVideo(1)

    				if contentchoice == 98:

    					print("""
    
    					quit : to quit the program
    
    					refresh : to refresh the song.
    
    					play : To play paused song again.
    
    					pause : To pause the song.
    
    					forward(time) : To skip a song forward to 'n' minutes.
    
    					backward(time) : To skip a song backward to 'n' minutes.
    
    						""")

    					cmd = input("[CMD] ");

    					if cmd == "quit" or cmd == "QUIT":
    						x.Close()
    					elif cmd == "help" or cmd == "HELP" or cmd == "=?":
    						x.HelpMenu()
    					elif cmd == "refresh" or cmd == "REFRESH":
    						x.RestartVideo()
    					elif cmd == "play" or cmd == "PLAY":
    						x.Play();
    					elif cmd == "pause" or cmd == "PAUSE":
    						x.Pause();
    					elif "forward" in cmd or "FORWARD" in cmd:
    						if ":" not in cmd:
    							x.MoveForward();

    						else:

    							Ftime = cmd.split(":")[1];
    							if(len(Ftime) == 0):
    								x.MoveForward()
    							else:
    								x.IncreaseTime = Ftime;
    								x.MoveForward()

    					elif "backward" in cmd or "Backward" in cmd:
    						if ":" not in cmd:
    							x.MoveBackwards();

    						else:

    							x.DecreaseTime = Ftime;
    							x.MoveBackwards()


    				elif contentchoice == 99:
    					x.existingProj = False;
    					continue

    				else:
    					x.NavigateYoutube(contentName)
    					x.PlayVideo(contentchoice);
    			else:
    				#no project prior running.

    				print("\n what do you want to listen? ");
    				speak("ok what do you want to listen?")
    				contentName = takeCommand()
    				

    				if contentName:
    					try:
    						x.NavigateYoutube(contentName)
    						x.ListVideos()

    					except:
    						pass

    		except ValueError:
    			pass


    		except common.exceptions.ElementClickInterceptedException:
    			speak("i am sorry i am unable to play ")
    			print("sorry can't play that.")
    			continue

    		except common.exceptions.WebDriverException:
    			print("Error while using Chrome Driver (Possible Causes ) : ");
    			print("1. Using Old Chrome Driver, Please Get Latest Version.")
    			print("2. Incorrect Path of Chrome Driver Provided, Please Correct It.")
    			input();
    			exit();



def sendEmail(to, content):
    """ instead of tying password in sendemail func, i stored it in a file and read from there to avoid password exposure"""
    file = open("emailpassword.txt", "r")
    emailpassword = file.read()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('harshit.singh.btech2020@sitpune.edu.in', emailpassword)
    server.sendmail('harshit.singh.btech2020@sitpune.edu.in', to, content)
    server.close()
    file.close()


def takeCommand():
    """it takes input from mic and returns string, #this function recognizes audio and converts in string, press ctrl
    and click on recogniser to adjust threshold energy according to noise in room..r.pause_threshold = 2 seconds of non speaking audio before a phrase is considered complete
        # so we"ll take 2 sec of max pause, you can access more things like energy etc in recognizer class ...
        some times listening takes a lot becuse energy threshold is high so it listens until little noise is there so reduce and if don't listen then vice versa"""
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try: #we use try when error can come so try if error comes then go to except
        print("Recognizing...")
        query = r.recognize_google(audio, language = 'en-in') #we used google recogniser , bing, sphinx are also available
        print("User said:", query)

    except Exception as e:
        print (e) #will print error if comes , if comment out error won't print
        print("Say that again please...")
        return 'None' #it's not return of function , it's returning a string saying 'None'
    return query
if __name__ == '__main__':
    wishMe()
    #while True:
    
    query= takeCommand().lower()
    #to execute task
    if 'wikipedia' in query :
        speak("Searching Wikipedia...")
        query = query.replace('wikipedia',"")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
        print("Do you want more details")
        speak("Do you want more details?")
        try:
            details = takeCommand().lower()
            if "yes" in details :
                speak("Ok giving more details")
                detailedresult = wikipedia.summary(query, sentences = 10)
                print(detailedresult)
                speak(detailedresult)

        except Exception as f :
            print("Sorry couldn't get you ", f)
            speak("Sorry could not get you")

    elif 'weather' in query:
        of = query.find("of")
        weather(query[of+3:])

    elif 'temperature' in query:
        of = query.find("of")
        weather(query[of+3:])

    elif 'humidity' in query:
        of = query.find("of")
        weather(query[of+3:])


    elif "take note" in query:
        nf = open("note.txt", "a")
        speak("ok what do you want to write in it?")
        content = takeCommand()
        nf.write("\n")
        nf.write(content)
        speak("notes written")
        nf.close()

    elif "show note" in query:
        fn = open("note.txt")
        speak("ok here are your notes")
        notes = fn.read()
        print(notes)
        fn.close()

    elif "delete note" in query:
        delfile = open("note.txt","w")
        delfile.truncate(0)
        delfile.close()
        speak("ok notes deleted")
        

    elif "hello" in query :

        speak("hello I am Robin , a desktop assistant created by harshit , how are you?")


    elif "play music" in query:
        print("opening music console...")
        play_music()



    #elif "weather" or "temperature" or "humidity" or "atmospheric pressure" and "of" in query:
    #    of = query.find("of")
    #    weather(query[of+3:])
                                                                                                 



    elif "send email" in query : #sending mail
        speak("Do you want to send mail to stored contacts?")
        print("Do you want to send mail to stored contacts?")
        ans = takeCommand().lower()
        if ans == "yes" :
            speak("Whom do you want to send?")
            person = takeCommand().lower()
            if "harshit" in person :
                receiver1= "harshit25102000@gmail.com"
                try:
                    speak("What you want to say in email")
                    content1 = takeCommand()

                    sendEmail(receiver1, content1)
                    speak("mail sent to Harshit")

                except Exception as e1:
                    print(e1)
                    speak("Sorry I am not able to send this email")

        else:

            try:

                speak("tell me the email address of receiver")
                to = takeCommand()
                speak("What you want to say in email")
                content = takeCommand()

                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry I am not able to send this email")





    elif 'open youtube' in query :
        speak("ok opening youtube")
        print("opening...")
        webbrowser.open('youtube.com')
    elif 'open google' in query :
        speak("ok opening google")
        print("opening...")
        webbrowser.open('google.com')
    elif 'open geeksforgeeks' in query :
        speak("ok opening geeksforgeeks")
        print("opening...")
        webbrowser.open('geeksforgeeks.com')
    elif "open stackoverflow" in query :
        speak("ok opening stackoverflow")
        print("opening...")
        webbrowser.open('stackoverflow.com')
    elif "open facebook" in query :
        speak("ok opening facebook")
        print("opening...")
        webbrowser.open('facebook.com')
    elif "open" and "com" in query:
        open = query.find("open")
        com = query.find("com")
        domain = query[open+4:com+4]
        speak(f"opening {query[open + 4:com + 4]}")
        print(f"opening {query[open + 4:com + 4]}")
        webbrowser.open(domain)

    elif "quote" in query:
        quotes()

    elif "joke" in query:
        jokes()

    elif 'the time' in query :
        strtime = datetime.datetime.now().strftime("%H:%M:%S")
        print(strtime)
        speak(f"sir the time is {strtime}")

    elif "the date" in query:
        today = time.strftime("%d/%m/%y")
        print(today)
        speak(f'sir the date is {today}')

    elif "news" in query and "about" in query:
        key = query.find("about")
        key_final = query[key+5:]
        specific_news(key_final)

    elif "news" in query:
        national_news()
    elif "open microsoft team" in query :
        teamspath =  r'C:\Users\Harshit Singh\AppData\Local\Microsoft\Teams\current\Teams.exe'
        speak("ok opening teams")
        os.startfile(teamspath)


    elif "open vs code" in query:
        codepath = "C:\\Users\\Harshit Singh\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        speak("ok opening VS code")

        os.startfile(codepath)

    elif "open disk c" in query:
        pathc = r"C:"
        speak("ok opening C disk")

        os.startfile(pathc)

    elif "open disk d" in query :
        pathd = "D:"
        speak("ok opening D disk")

        os.startfile(pathd)

    elif "open telegram" in query:
        telegrampath = r'C:\Users\Harshit Singh\AppData\Roaming\Telegram Desktop\telegram.exe'
        speak("ok opening telegram")

        os.startfile(telegrampath)


    #elif "open snakes in pycharm" or 'open snakes' in query:
    #    codepath = r'C:\Users\Harshit Singh\PycharmProjects\pygametut\snake.py'
    #    speak("ok opening snakes")
    #
    #    os.startfile(codepath)


    else:
        print("last case")                       #if nothing matches show google search result
        if "robin" in query:
            term = query.replace("robin", "")
            new =2
            speak("Sorry I did not get you , showing you the web result of your query")
            print("opening google to find your query")
            taburl = "http://google.com/search?q=";

            webbrowser.open(taburl+term,new=new) ;

        else :
            speak("Sorry I did not get you , showing you the web result of your query")
            print("opening google to find your query")
            taburl = "http://google.com/search?q=";
            new=2
            webbrowser.open(taburl+query,new=new) ;





















































































































































































