import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os
import winsound
from utils_qna import *
import pyttsx3

load_dotenv()
speech_key = os.environ.get("SPEECH_KEY")
service_region = os.environ.get("SPEECH_REGION")
model = os.environ['OPENAI_QnA_MODEL'] #e.g. 'text-davinci-003' deployment

initialize()
remember=''
rememberAI=''
context=''
text=''
winsound.Beep(440, 200)
openai_replied=False
for i in range (16):
    if openai_replied: 
        winsound.Beep(140, 200)
        rememberAI+=reply_text
        colorprint('remembering','60')
        #tts_nofile('Remembering')
        openai_replied=False
    text=from_mic()
    print(text)
    #if text=='Ok.': 
    #    print('Im here')
    #    remember+="\n"+reply_text
    

    if (text[:8] in ['Remember','Remind m']) and len(text)>12:
        openai_replied=False
        remember+="\n"+text[10:]
        context = context+'\n'+text[10:]
        print('Rememering: '+text[9:])
        #winsound.Beep(440, 200)
    if (text[-1]=='?'):
       # tts_nofile('Sending your question to OpenAI. '  ,rate=200,volume=0.06,pitch=-5)
        reply=get_completion(prompt=context+'\n\n'+text,model=model,max_tokens=90)
        reply_text = reply[1]['choices'][0]['text'].encode().decode()
        tts_nofile(reply_text)
        
        openai_replied= True
        context=remember + '\n'+reply_text
        #if from_mic()[0:2]=='yes': remember+="\n"+reply_text
        #colorprint(reply_text)
    if (text =='OK, stop.'): 
        tts_nofile(' Bye!')
        break
    if (text in ['Hi.','Hello.']): 
        tts_nofile('Hello, Nice to see you')
    if (text=='Show me what you remember.'):
        print(remember)
        print('----')
    if (text=='Show me context.'):
        print(context)
        print('----')
    if (text=='Remember it.'):
        remember+=reply_text
    if (text=='Delete memory.'):
        remember =''
        rememberAI=''
    if (text=='Stop this nonsense.'):context=remember
    if (text == 'Show me special instructions.'):
        print('OK, stop. - to end the program')
        print('Remember: <any text>')
        print('Show me what you remember.')
        print('Delete memory.')
        print('Remember it. - for latest reply from OpenAi')
        print('Stop this nonsense. - to erease latest reply from context')

print('-------------------------------------------')
print(remember)
colorprint(rememberAI)
