import re
import random
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
BOT_GREETING_MESSAGES = [
    "Hello! How can I assist you today?",
    "Hi! What would you like help with?",
    "Hey there! How may I support you?"
]
BOT_DESCRIPTION_LINES = [
    "I'm a lightweight chatbot built using Python and Tkinter.",
    "I'm just a basic rule-driven chatbot that replies based on patterns.",
    "I'm a tiny pattern-matching bot — no cloud learning, just simple logic!"
]
BOT_HELP_MESSAGES = [
    "Of course — just let me know what you need help with.",
    "Happy to assist! What would you like to do?",
    "I can answer basic questions like the current time, date, greetings, or farewells."
]
BOT_FALLBACK_REPLIES = [
    "Sorry, I couldn't quite understand that. Could you try phrasing it differently?",
    "Hmm... I’m not sure how to respond to that yet.",
    "I didn't catch that — maybe ask in another way?"
]
BOT_FAREWELL_LINES = [
    "Goodbye! Have a wonderful day!",
    "See you later — take care!",
    "Bye! It was nice talking to you."
]
def chatbot_response(user_input: str) -> str:
    """
    Processes the user's message and returns an appropriate reply.
    All logic stays identical to the original version.
    """
    processed_text = user_input.lower().strip()
    if re.search(r'\b(hi|hello|hey|hiya)\b', processed_text):
        return random.choice(GREETINGS)
    if re.search(r'\b(who are you|what are you|about you)\b', processed_text):
        return random.choice(ABOUT_BOT)
    if re.search(r'\b(help|support|assist|how to)\b', processed_text):
        return random.choice(BOT_HELP_MESSAGES)
    if re.search(r'\b(time|current time|what time)\b', processed_text):
        current_time = datetime.now().strftime("%H:%M:%S")
        return f"The current time is {current_time}."
            if re.search(r'\b(date|day|today)\b', processed_text):
        today_date = datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {today_date}."

    math_match = re.search(r'(\bwhat is\b|\bcalculate\b)\s*([\d\.\s\+\-\*\/\(\)]+)', processed_text)
    if math_match:
        expression = math_match.group(2)
        if re.fullmatch(r'[\d\.\s\+\-\*\/\(\)]+', expression):
            try:
                result = eval(expression, {"__builtins__": {}})
                return f"The answer is {result}"
            except Exception:
                return "I couldn't calculate that expression."
        else:
            return "I can only calculate simple numeric expressions."
    if re.search(r'\b(bye|goodbye|exit|quit|see you)\b', processed_text):
        return random.choice(BOT_FAREWELL_LINES)
    return random.choice(BOT_FALLBACK_REPLIES)
class RuleChatGUI:
    def __init__(self, root):
        self.root = root
        root.title("Rule-Based Chatbot")
        root.geometry("520x500")
        root.resizable(False, False)
        self.chat_display = scrolledtext.ScrolledText(
            root, state='disabled', wrap='word', font=("Helvetica", 11)
        )
        self.chat_display.place(x=10, y=10, width=500, height=380)
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(root, textvariable=self.entry_var, font=("Helvetica", 12))
        self.entry.place(x=10, y=405, width=380, height=35)
        self.entry.bind("<Return>", self.on_send)
        self.send_btn = tk.Button(root, text="Send", command=self.on_send, width=10)
        self.send_btn.place(x=400, y=405, width=110, height=35)
        self._append_chat("Chatbot", " Hello! Type 'bye' to end the chat.")
    def _append_chat(self, sender: str, message: str):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)
    def on_send(self, event=None):
        user_text = self.entry_var.get().strip()
        if not user_text:
            return
        self._append_chat("You", user_text)
        self.entry_var.set("")
        response = chatbot_response(user_text)
        self._append_chat("Chatbot", response)
        if re.search(r'\b(bye|goodbye|exit|quit|see you)\b', user_text.lower()):
            self.root.after(1200, self.root.destroy)
if __name__ == "__main__":
    root = tk.Tk()
    app = RuleChatGUI(root)
    root.mainloop()
