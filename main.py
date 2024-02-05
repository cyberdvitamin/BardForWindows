from bardapi import Bard
from bardapi import BardCookies
import os
import time
import tkinter as tk


# de mutat in alt fisier also check from time to time in caz ca se schimba
cookie_dict = {
    "__Secure-1PSID": "fgiU1Z6BVOBeqBSkGyjZTX7WDGUB62iVbU98IrmJGfuT_emDxVQaCkXmUJ33Ev6Hhiekdg.",
    "__Secure-1PSIDTS": "sidts-CjEBPVxjSkGCoV6uxjYrOUgL4jS-DF_xDek7wemHWgW0aBSayaOh7JPuRMeLLuyvKE-1EAA",
    "__Secure-1PSIDCC":"ABTWhQHKjiLdCgZ8Q2VwPV5x33Wrz-z0z3nDD8q_iq9gDtzb_ejMS7Yof_lnJJvozOqoST_h0LEg"
}

bard = BardCookies(cookie_dict=cookie_dict)
# Get the current time as a struct_time object
current_time = time.localtime()

# Format the time as a string in the 24-hour format
formatted_time = time.strftime("%H:%M", current_time)


# Function to handle button click and display chatbot response
def send_message():
    user_input = entry_field.get()
    entry_field.delete(0, tk.END)  # Clear the entry field
    chat_history.tag_configure("bold_font", font=("Arial", 12,"bold"))
    chat_history.tag_configure("normal_font", font=("Arial", 12 ,"normal"))
    chat_history.insert(tk.END, formatted_time + " You: " + user_input + "\n", "bold_font")
    chat_history.insert(tk.END, formatted_time + " You: ", "bold_font")
    chat_history.insert(tk.END, user_input + "\n", "normal_font")

    # Replace this with your chatbot's response generation logic
    #chatbot_response = bard.get_answer(str(user_input))['content']  # Replace this with your chatbot's response function
    #chat_history.insert(tk.END, formatted_time + " Bard: " + chatbot_response + "\n")

# Create the main window
root = tk.Tk()
root.title("Bard for Windows")

# Create the text area for displaying chat history
chat_history = tk.Text(root, width=50, height=20, wrap=tk.WORD)
chat_history.pack(pady=10)

# Create the entry field and button
entry_field = tk.Entry(root, width=40)
entry_field.pack(side=tk.LEFT, padx=10)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT, padx=10)

# Start the chat with a greeting
chat_history.insert(tk.END, formatted_time + " Bard: Hello! How can I help you today?\n")

# Run the Tkinter main loop
root.mainloop()
