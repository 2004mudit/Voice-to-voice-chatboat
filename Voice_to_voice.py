import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import time

class GeminiVoiceChatbot:
    def __init__(self):
        # ============= PUT YOUR API KEY HERE =============
        GEMINI_API_KEY = "AIzaSyCVSALZAtjSWof5WlcG-TyL93Uc7MQVN0Y"  # Replace with your actual API key
        # ===============================================
        
        try:
            # Initialize Gemini
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
            
            # Initialize speech recognizer
            self.recognizer = sr.Recognizer()
            
            # Initialize text-to-speech engine
            self.engine = pyttsx3.init()
            
            # Configure voice - More explicit female voice selection
            voices = self.engine.getProperty('voices')
            female_voice_set = False
            
            # Try to find and set a female voice
            for voice in voices:
                if any(keyword in voice.name.lower() for keyword in ['female', 'woman', 'girl', 'zira']):
                    self.engine.setProperty('voice', voice.id)
                    female_voice_set = True
                    print(f"Using female voice: {voice.name}")
                    break
            
            if not female_voice_set:
                print("No female voice found. Using default voice.")
            
            # Additional voice properties for more natural speech
            self.engine.setProperty('rate', 145)     # Slightly slower
            self.engine.setProperty('volume', 0.85)  # Slightly softer
            
            print("Initialization successful! Chatbot is ready.")
            
        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            print("Please check if your API key is correct and all requirements are installed.")
            raise

    def listen(self):
        """Listen to user's voice input"""
        with sr.Microphone() as source:
            print("\nListening... Speak now!")
            # Reduce ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("Processing your speech...")
                
                try:
                    # Using Google's free speech recognition API
                    text = self.recognizer.recognize_google(audio)
                    print(f"You said: {text}")
                    return text
                except sr.UnknownValueError:
                    print("Could not understand audio. Please try again.")
                    return None
                except sr.RequestError as e:
                    print(f"Speech recognition error: {e}")
                    return None
                    
            except sr.WaitTimeoutError:
                print("No speech detected. Please try again.")
                return None

    def get_gemini_response(self, user_input):
        """Get response from Gemini AI"""
        try:
            # Add current time context and instructions for time-related queries
            current_time_context = f"The current time is {time.strftime('%I:%M %p')} {time.strftime('%Z')}. "
            prompt = f"""Please provide a brief, conversational response in 1-2 short sentences. 
            If asked about time, use this accurate current time: {current_time_context}
            Keep it simple and focus on the most important information.
            Question: {user_input}"""
            
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            print(f"Error getting Gemini response: {e}")
            return "I apologize, but I encountered an error."

    def speak(self, text):
        """Convert text to speech with natural breaks"""
        try:
            print("\nAI:", text)
            
            # Split text into sentences
            sentences = text.replace('!', '.').replace('?', '?|').replace('.', '.|').split('|')
            
            for sentence in sentences:
                if sentence.strip():  # Skip empty sentences
                    self.engine.say(sentence.strip())
                    self.engine.runAndWait()
                    
                    # Add a small pause between sentences
                    time.sleep(0.5)  # Adjust pause duration (in seconds) as needed
                    
            # Add a longer pause at the end of the complete response
            time.sleep(1)
            
        except Exception as e:
            print(f"Text-to-speech error: {e}")
            print("Text response:", text)

    def run(self):
        """Main loop for the chatbot"""
        print("\n=== Gemini Voice Chatbot Started ===")
        print("Tips:")
        print("- Speak clearly into your microphone")
        print("- Say 'exit', 'quit', or 'bye' to end the conversation")
        print("- Wait for the 'Listening...' prompt before speaking")
        print("=====================================\n")
        
        self.speak("Hello! I'm your AI voice assistant powered by Gemini. How can I help you today?")
        
        while True:
            user_input = self.listen()
            
            if user_input:
                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    self.speak("Goodbye! Have a great day!")
                    break
                
                # Get response from Gemini
                response = self.get_gemini_response(user_input)
                self.speak(response)

def main():
    try:
        chatbot = GeminiVoiceChatbot()
        chatbot.run()
    except Exception as e:
        print("\nError starting the chatbot:")
        print(str(e))
        print("\nPlease make sure:")
        print("1. You've replaced the API key with your actual Gemini API key")
        print("2. All required packages are installed:")
        print("   pip install google-generativeai SpeechRecognition pyttsx3 pyaudio")
        print("3. Your microphone is properly connected and working")
        print("4. You have an active internet connection")

if __name__ == "__main__":
    main()