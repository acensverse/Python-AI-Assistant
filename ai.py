import speech_recognition as sr
import pyttsx3
import openai
from config import apikey
import os

# OpenAI code
def chat(query, chat_str):
    try:
        openai.api_key = apikey
        chat_str += f"Me: {query}\nAI: "
        chat_str += f"Openai responses for Prompt: {query} \n **********************\n\n"
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct-0914",
            prompt=chat_str,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        chat_str += f"{response['choices'][0]['text']}\n"
        print(chat_str)
        say(response["choices"][0]["text"]) 

        if not os.path.exists("Openai"):
            os.mkdir("Openai")

        with open(f"Openai/{query[0:30]}.txt", "w") as f:
            f.write(chat_str)

    except Exception as e:
        print(f"An error occurred while interacting with OpenAI: {e}")
    return chat_str

# Engine functions
def say(text):
    engine = pyttsx3.init(driverName='espeak')  # Linux voice engine 
    #engine.setProperty('voice', engine.getProperty('voices')[0].id) #Windows voice engine 
    engine.setProperty('voice', 'm1')
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# Initialize recognizer
recognizer = sr.Recognizer()

# Initialize chatStr
chatStr = ""

# Use the microphone as the audio source
while True:
    with sr.Microphone() as source:
        print("Please start speaking...")

        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)

        try:
            # Listen to the speech and store it in audio_text variable
            audio_text = recognizer.listen(source)
            print("Audio recording complete.")

            # Use Google Speech Recognition to convert audio to text
            recognized_text = recognizer.recognize_google(audio_text)

            if recognized_text:
                print("Recognized text: " + recognized_text)
                # Update chatStr using the chat function
                chatStr = chat(recognized_text, chatStr)

                 # Check if the user wants to stop the conversation
                if recognized_text.lower() == "stop":
                    print("Conversation stopped.")
                    break  # Exit the loop
            else:
                print("Sorry, I did not understand what you said.")

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio.")

        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

