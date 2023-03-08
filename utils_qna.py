import openai
import os
import winsound
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import pyttsx3

def colorprint(txt,opt="222",end='\n'): 
    #print(f'\033[{opt}m',txt,'\033[0m',end=end)
    print(u"\u001b[38;5;"+opt+'m'+txt+u"\u001b[0m",end=end)

def initialize(engine='text-ada-001'):

    openai.api_type = "azure"
    openai.api_base = os.getenv('OPENAI_API_BASE')
    openai.api_version = "2022-12-01"
    openai.api_key = os.getenv("OPENAI_API_KEY")

    print("openai.api_type: "+openai.api_type)
    print("openai.api_base: "+ openai.api_base)
    print("openai.api_version: "+openai.api_version)
    print("openai.api_key: "+'***')


# Semantically search using the computed embeddings locally


load_dotenv()
speech_key = os.environ.get("SPEECH_KEY")
service_region = os.environ.get("SPEECH_REGION")
model = os.environ['OPENAI_QnA_MODEL'] #e.g. 'text-davinci-003' deployment

def from_mic():
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    #winsound.Beep(240, 200)
    result = speech_recognizer.recognize_once_async().get()
    text=result.text
    return(text)

def tts_nofile(text='Python',rate=200,volume=0.02,voice_idx=1):
    engine = pyttsx3.init()
    voice = engine.getProperty('voices')
    #2. 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
    '''
    for voice in engine.getProperty('voices'):
        print('voice.id:'+voice.id)
        print(voice)
    '''    
    engine.setProperty('voice', voice[1].id )
    engine.setProperty('rate', rate)
    engine.setProperty('volume',volume)
 
   


    #engine.setProperty()
    
    engine.say(text)
    # play the speech
    engine.runAndWait()


def get_completion(prompt="", max_tokens=400, model="text-davinci-003"):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=1,
        max_tokens=max_tokens,
        top_p=0.5,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    colorprint(f"{response['choices'][0]['text'].encode().decode()}")

    return prompt,response#, res['page'][0]







