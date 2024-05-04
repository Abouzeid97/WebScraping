#Dependencies
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
import pytz
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
Hello world :)
this a simple example of webscraping using selenium libraries

Beside that twitter has no longer shows posts from user profiles in reverse chronological order.
In other words, it randomizes the order of the tweets. only if the user has logged in

I used as a test case using the given twitter accounts the time frame = 250,000 minutes apparently 3/12/2023

So I can collect data from twitter.

I hope this meet your expectations.

Sherif Abouzeid

sherif.abouzeid@gmail.com

"""


#Function to check if the tweet is pinned
def CheckPinned(tweet):
    sleep(5)
    tweet_element = None
    try:
        tweet_element = tweet.find_element(By.XPATH, ".//div[@data-testid='socialContext']")
    except:
        pass
    if tweet_element:
        return True
    else:
        return False

#Function to convert time to the our timezone and calculate the time difference and return it in minutes
def TimeZone(time):
    timestamp = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    timestamp_utc = timestamp.replace(tzinfo=pytz.utc)
    
    cairo_timezone = pytz.timezone('Africa/Cairo')

    timestamp_cairo = timestamp_utc.astimezone(cairo_timezone)
   
    current_time_cairo = datetime.now(cairo_timezone)

    time_difference = current_time_cairo - timestamp_cairo

    minutes_difference = int(time_difference.total_seconds() / 60)
    return minutes_difference

#Function to check if the tweet within the time interval
def CheckTimeInterval():
    if TweetTime < time_frame:
        return True
    else:
        return False

#Function to check if the tweet text has the Ticker  example $SPX
def CheckTicker(driver):
    
    tweet_text_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, ".//div[@data-testid='tweetText']"))
    )

    tweet_text = tweet_text_element.text.lower()
    if ticker in tweet_text:
        return True
    else:
        return False 

#Function to check if the tweet has the "show more" span to handle it    
def CheckShowMore(tweet):
    sleep(5)
    span_element = None
    try:
        span_element = tweet.find_element(By.XPATH, ".//a[@data-testid='tweet-text-show-more-link']")
    except:
        pass
    if span_element:
        href = span_element.get_attribute("href")
        driver.get(href)
        return True
    else:
        return False
    
#The user enters the twitter accounts serpareted to spaces and then we convert them as a list of accounts
input_string = input("Enter twitter accounts separated by spaces: ")
TwitterAccounts = input_string.split()

#The user enters the ticker using the Cashtag '$' and then we convert it to lower case
ticker = input("Enter the ticker using the Cashtag '$': ")
ticker = ticker.lower()

#The user enters the time interval in minutes for the scraping session
time_frame = int(input("Enter the time interval in minutes for the scraping session: "))

#Initialize WebDriver and maximize the window
driver = webdriver.Chrome()
driver.maximize_window()
TweetAdded = []

#Looping through all the twitter accounts
counter = 0
for i in range(0, len(TwitterAccounts)):

    #Open the Twitter profile page
    driver.get(f"https://www.twitter.com/" + TwitterAccounts[i])
    sleep(5)
    tweets = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
   
    #Looping through all the tweets of the twitter account
    for j, tweet in enumerate(tweets):
        #using a javascript function to scroll down each iteration
        driver.execute_script(f"window.scrollBy(0, {600});")
        sleep(2)
        if CheckPinned(tweet):
            time = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ".//time"))
            )
            TweetTime = time.get_attribute('datetime')
            TweetTime = TimeZone(TweetTime)

            if CheckTimeInterval():
                if CheckTicker(driver) and tweet not in TweetAdded:
                    counter +=1
                    TweetAdded.append(tweet)

        else:
            time = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ".//time"))
            )
            TweetTime = time.get_attribute('datetime')
            TweetTime = TimeZone(TweetTime)

            if CheckTimeInterval():
                if CheckShowMore(tweet):
                        
                    if CheckTicker(driver) and tweet not in TweetAdded:
                        counter +=1
                        TweetAdded.append(tweet)
                    
                    driver.execute_script("window.history.go(-1)")
                    driver.back()
                    tweets = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")[j+1:]
                    sleep(5)
                    break
                        
                elif CheckTicker(driver) and tweet not in TweetAdded:
                    counter +=1
                    TweetAdded.append(tweet)  
            else:
                break
              
            
driver.quit()
#The output
print(f"the " + ticker + " was mentioned " + str(counter) + " times in the last " + str(time_frame) + " minutes")               

