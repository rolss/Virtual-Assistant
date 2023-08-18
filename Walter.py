import pyttsx3
import speech_recognition as sr
import re
import wikipedia
import datetime

"""
COMMANDS

Walter say Hello
Walter say *something*
Walter wikipedia *something*
"""
engine = pyttsx3.init('sapi5') 
# engine.setProperty('rate', 210) # default rate is 200
activationWord = 'walter'
mic = sr.Microphone()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def parseCommand():
    listener = sr.Recognizer()
    print('Listening...')

    with mic as source:
        listener.pause_threshold = 1
        input_speech = listener.listen(source)
    try:
        print('Recognizing...')
        input_text = listener.recognize_google(input_speech)
        print("You said:", input_text)
    except Exception as exception:
        print('Sorry, I could not understand')
        speak('Sorry, I could not understand')
        print(exception)
        return 'None'
    return input_text

def wikiSearch(query = ''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        return 'Nothing could be found'
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    wikiSummaryCut = cut_text(wikiSummary, 500)
    return wikiSummaryCut

def cut_text(text, maxcharacters):
    if len(text) > maxcharacters:
        # Find last period within text size
        last_period = text.rfind('.', 0, maxcharacters)
        
        # Cut text up until that last period
        if last_period != -1:
            cut_text = text[:last_period + 1]
            return cut_text
    return text

if __name__ == '__main__':
    speak('Hey, I am Walter.')

    while True:
        input_text = parseCommand().lower().split()

        if input_text[0] == activationWord:
            input_text.pop(0)

            if input_text[0] == 'say':
                if 'hello' in input_text:
                    speak('Hello!')
                else:
                    input_text.pop(0) # remove say
                    speech = ' '.join(input_text)
                    speak(speech)

            if input_text[0] == 'wikipedia':
                input_text = ' '.join(input_text[1:])
                speak('Searching your query...')
                wikiResult = wikiSearch(input_text)
                speak(wikiResult)

            if input_text[0] == 'new' and input_text[1] == 'birthday':
                speak("Please tell me the month and day of the birthday.") # February the 21st or February 21
                birth_date = parseCommand().lower() # get requested birthday
                
                birth_date = birth_date.replace('the', '') # clean query if required
                birth_date = birth_date.split() # birth_date[0] - month, birth_date[1] - day

                # regex finds if numbers are in '1st, 2nd, 3rd, 4th' format and strips the characters by keeping only the digits
                birth_date[1] = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', birth_date[1])

                speak(f"I have written it down as {birth_date[0]} {birth_date[1]}. Can I get a name for this?")
                birth_date.append(parseCommand().lower())

                date_to_save = ','.join(birth_date)
                with open('birthdays.txt', 'a') as file:
                    file.write(date_to_save)
                    speak("Birthday successfully added")

            if input_text[0] == 'birthdays':
                with open('birthdays.txt', 'r') as file:
                    lines = file.readlines()
                    today = datetime.date.today()
                    today_split = today.strftime(f"%B {today.day}").split()
                    filtered_birthdays = [element for element in lines if (today_split[0].lower() in element and today_split[1] in element)]
                    
                    if filtered_birthdays:
                        for birthday in filtered_birthdays:
                            birthday = birthday.strip().split(',')
                            speak(f"{birthday[2]}'s birthday is today")
                            print(birthday[2].strip())
                    else:
                        speak("No birthdays today!")
                    
                    
                        
                


            if input_text[0] == 'exit':
                speak('See you later, have a good day')
                break