from bardapi import Bard
import os
import time
import tkinter as tk
import requests
import bardToken
import seleniumGoogleLogin
import undetected_chromedriver as uc
from dotenv import load_dotenv

class BardApiHandler:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Get environment variables
        self.BARD_API_KEY = os.getenv("BARD_API_KEY")
        self.USERNAME = os.getenv("GMAIL")
        self.PASSWORD = os.getenv("PASSWORD")

    def cache_credentials(self, api_key, username, password):
        # Cache credentials to .env file
        with open(".env", "w") as env_file:
            env_file.write(f"BARD_API_KEY={api_key}\n")
            env_file.write(f"GMAIL={username}\n")
            env_file.write(f"PASSWORD={password}\n")

    def get_bard_api(self):
        try:
            Bard(token=self.BARD_API_KEY)
        except:
            # Use selenium to get BARD_API_KEY if invalid/old & Cache.
            driver = uc.Chrome()
            driver.delete_all_cookies()

            if seleniumGoogleLogin.start(driver, self.USERNAME, self.PASSWORD):
                self.BARD_API_KEY = bardToken.get(driver)  # Get bard token
                # Cache key, username, and password
                self.cache_credentials(self.BARD_API_KEY, self.USERNAME, self.PASSWORD)
                # Close browser
                driver.quit()
        finally:
            # Setup browser session
            session = requests.Session()
            session.headers = {
                "Host": "bard.google.com",
                "X-Same-Domain": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/91.0.4472.114 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "Origin": "https://bard.google.com",
                "Referer": "https://bard.google.com/",
            }
            session.cookies.set("__Secure-1PSID", self.BARD_API_KEY)
            return Bard(token=self.BARD_API_KEY, session=session)


bard_handler = BardApiHandler()
bard = bard_handler.get_bard_api()

# Get the current time as a struct_time object
current_time = time.localtime()

# Format the time as a string in the 24-hour format
formatted_time = time.strftime("%H:%M", current_time)

# Function to handle button click and display chatbot response
def send_message():
    user_input = entry_field.get()
    entry_field.delete(0, tk.END)  # Clear the entry field
    chat_history.tag_configure("bold_font", font=("Quitars", 18,"bold"))
    chat_history.tag_configure("normal_font", font=("Quitars", 15 ,"normal"))
    chat_history.insert(tk.END, formatted_time + " You: ", "bold_font")
    chat_history.insert(tk.END, user_input + "\n", "normal_font")

    # Replace this with your chatbot's response generation logic
    chatbot_response = bard.get_answer(str(user_input))['content']  # Replace this with your chatbot's response function
    chat_history.insert(tk.END, formatted_time + " Bard: ", "bold_font")
    chat_history.insert(tk.END, chatbot_response + "\n", "normal_font")

# Create the main window
root = tk.Tk()
root.title("Bard for Windows")

# Create the text area for displaying chat history
chat_history = tk.Text(root, width=60, height=25, wrap=tk.WORD)
chat_history.pack(pady=10)

# Create the entry field and button
entry_field = tk.Entry(root, width=50)
entry_field.pack(side=tk.LEFT, padx=15)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT, padx=10)

chat_history.tag_configure("bold_font", font=("Quitars", 18,"bold"))
chat_history.tag_configure("normal_font", font=("Quitars", 15 ,"normal"))

# Start the chat with a greeting
chat_history.insert(tk.END, formatted_time + " Bard: ", "bold_font")
chat_history.insert(tk.END, "Hello! How can I help you today?\n", "normal_font")

# Run the Tkinter main loop
root.mainloop()
