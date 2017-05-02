import scrapy
import random
import time
import io
import requests
import os
from time import sleep

from pydub import AudioSegment
import speech_recognition as sr

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException

MIN_RAND = 0.64
MAX_RAND = 1.27
LONG_MIN_RAND   = 4.78
LONG_MAX_RAND   = 11.1
FIREFOX_BIN_PATH = "/Applications/Firefox.app/Contents/MacOS/firefox-bin"

DIGITS_DICT = {
                "zero": "0",
                "one": "1",
                "two": "2",
                "three": "3",
                "four": "4",
                "five": "5",
                "six": "6",
                "seven": "7",
                "eight": "8",
                "nine": "9",
                }


HOUNDIFY_CLIENT_ID = os.environ.get('HOUNDIFY_CLIENT_ID')
HOUNDIFY_CLIENT_KEY = os.environ.get('HOUNDIFY_CLIENT_KEY')

visited_urls = set()

class Sgpbusiness(scrapy.Spider):
    name = 'sgpbusiness'
    start_urls = ['https://www.sgpbusiness.com/browse/A']

    def __init__(self, *a, **kw):
        super(Sgpbusiness, self).__init__(*a, **kw)
        self.driver = webdriver.Firefox(firefox_binary=FirefoxBinary(FIREFOX_BIN_PATH))

    def is_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        except:
            return False

        return True

    def get_audio_challenge(self, iframes):
        # Switch to the last iframe (the new one)
        self.driver.switch_to_frame(iframes[-1])
        
        # Check if the audio challenge button is present
        if not self.is_exists_by_xpath('//button[@id="recaptcha-audio-button"]'):
            print("No element of audio challenge!!")
            return False
        
        print("Clicking on audio challenge")
        # Click on the audio challenge button
        self.driver.find_element_by_xpath('//button[@id="recaptcha-audio-button"]').click()
        time.sleep(random.uniform(LONG_MIN_RAND, LONG_MAX_RAND))


    def get_challenge_audio(self, url):
        # Download the challenge audio and store in memory
        request = requests.get(url)
        audio_file = io.BytesIO(request.content)
        
        # Convert the audio to a compatible format in memory
        converted_audio = io.BytesIO()
        sound = AudioSegment.from_mp3(audio_file)
        sound.export(converted_audio, format="wav")
        converted_audio.seek(0)
        
        return converted_audio


    def speech_to_text(self, audio_source):
        # Initialize a new recognizer with the audio in memory as source
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_source) as source:
            audio = recognizer.record(source) # read the entire audio file

        audio_output = ""
        # recognize speech using Google Speech Recognition
        try:
            audio_output = recognizer.recognize_google(audio)
            print audio_output
            print("Google Speech Recognition: ")
            # Check if we got harder audio captcha
            if any(character.isalpha() for character in audio_output):
                # Use Houndify to detect the harder audio captcha
                print("Fallback to Houndify!")
                audio_output = self.string_to_digits(recognizer.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY))
                print("Houndify: ")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service;")
        
        print audio_output    
        return audio_output


    def string_to_digits(self, recognized_string):
        return ''.join([DIGITS_DICT.get(word, "") for word in recognized_string.split(" ")])


    def solve_audio_challenge(self):
        # Verify audio challenge download button is present
        if not self.is_exists_by_xpath('//a[@class="rc-audiochallenge-download-link"]') and \
                not self.is_exists_by_xpath('//div[@class="rc-text-challenge"]'):
            print("No element in audio challenge download link!!")
            return False
        
        # If text challenge - reload the challenge
        while self.is_exists_by_xpath('//div[@class="rc-text-challenge"]'):
            print("Got a text challenge! Reloading!")
            self.driver.find_element_by_id('recaptcha-reload-button').click()
            time.sleep(random.uniform(MIN_RAND, MAX_RAND))

        # Get the audio challenge URI from the download link
        download_object = self.driver.find_element_by_xpath('//a[@class="rc-audiochallenge-download-link"]')
        download_link = download_object.get_attribute('href')
        
        # Get the challenge audio to send to Google
        converted_audio = self.get_challenge_audio(download_link)
        
        # Send the audio to Google Speech Recognition API and get the output
        audio_output = self.speech_to_text(converted_audio)

        # Enter the audio challenge solution
        self.driver.find_element_by_id('audio-response').send_keys(audio_output)
        time.sleep(random.uniform(LONG_MIN_RAND, LONG_MAX_RAND))

        # Click on verify
        self.driver.find_element_by_id('recaptcha-verify-button').click()
        time.sleep(random.uniform(LONG_MIN_RAND, LONG_MAX_RAND))
        
        return True

    def break_recaptcha_challenge(self):
        # Switch to page's main frame
        sleep(5)
        self.driver.switch_to.default_content()

        # Get all the iframes on the page
        iframes = self.driver.find_elements_by_tag_name("iframe")

        # Get audio challenge
        self.get_audio_challenge(iframes)

        # Solve the audio challenge
        if not self.solve_audio_challenge():
            return False

        # Check if there is another audio challenge and solve it too
        while self.is_exists_by_xpath('//div[@class="rc-audiochallenge-error-message"]') and \
                self.is_exists_by_xpath('//div[contains(text(), "Multiple correct solutions required")]'):
            print("Need to solve more. Let's do this!")
            self.solve_audio_challenge()

        # Switch to the reCAPTCHA iframe to verify it is solved
        #self.driver.switch_to.default_content()
        # self.driver.switch_to_frame(iframes[0])    

        # if self.is_exists_by_xpath('//span[@aria-checked="true"]'):
        #     print "THEY BEAT THE AUDIO CHALLENGE!!!"    
        #     return True

        # else:
        #     print "It failed"
        #     return False   
        return True

    def parse(self, response):
        # if response.url in visited_urls:
        #     print "It's a duplicate URL"
        #     return 

        if response.xpath('//div[contains(@class,"g-recaptcha")]').extract():
            print "Found reCAPTCHA on the page"
            self.driver.get(response.url)
            elem = self.driver.find_element_by_xpath('//iframe')
            self.driver.switch_to_frame(elem)
            time.sleep(random.uniform(MIN_RAND, MAX_RAND))
            self.driver.find_element_by_xpath('//span[contains(@class, "recaptcha-checkbox goog-inline-block") and @role="checkbox"]').click()
            time.sleep(random.uniform(MIN_RAND, MAX_RAND))

            if self.is_exists_by_xpath('//span[@aria-checked="true"]'):
                print "No challenge. Request for same url"
                yield scrapy.Request(url=response.url, callback=self.parse, dont_filter=True)
                return
            else:
                print "reCAPTCHA challenge"
                beaten = self.break_recaptcha_challenge() 
                #self.driver.switch_to.default_content()

                if beaten:
                    print "yield new request"
                    yield scrapy.Request(url=response.url, callback=self.parse, dont_filter=True)
                    return
                else:
                    return    

        visited_urls.add(response.url)
        for page_url in response.xpath('//li[contains(@class, "next")]/a/@href').extract():
            page_url = response.urljoin(page_url)
            yield scrapy.Request(url=page_url, callback=self.parse, dont_filter=True)

        for company in response.xpath('//div[contains(@class, "list-group")]//a'):
            yield {
                'company_name': company.xpath('child::h5/text()').extract_first()
            }   