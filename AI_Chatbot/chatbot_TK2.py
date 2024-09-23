import os
import customtkinter as ctk
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the Groq API key from the environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize the Groq client with the API key
client = Groq(api_key=GROQ_API_KEY)

# Define a consistent system prompt to guide the model
def get_system_prompt(assistant_type):
    return {
        "role": "system",
        "content": f"You are a {assistant_type}. Please know your role clearly. Please be informative, factual and concise. Please refuse to answer any questions irrelevant to who you are."
    }

class ChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("JANSOC v1.0")
        self.geometry("500x500")

        # Frame for the top row
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(side="top", fill="x")

        # Title label anchored at the top left
        title_label = ctk.CTkLabel(top_frame, text="JANSOC", font=("Arial", 16))
        title_label.pack(side="left", padx=12, pady=10)

        # Combo box anchored at the top right
        self.combo_box = ctk.CTkOptionMenu(top_frame, values=["General Assistant", "Code Assistant", "Travel Assistant"], command=self.update_prompt)
        self.combo_box.pack(side="right", padx=(0, 10), pady=10)

        # Create a text area to display the conversation
        self.conversation_area = ctk.CTkTextbox(self, wrap="word", state="disabled")
        self.conversation_area.pack(pady=10, padx=10, fill="both", expand=True)

        # Frame for input and send button
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10, padx=10, fill="x")

        # Create an entry field for user input
        self.user_input = ctk.CTkEntry(input_frame, placeholder_text="Enter your prompt here...")
        self.user_input.pack(side="left", fill="x", expand=True)

        # Create a button to send the prompt
        self.send_button = ctk.CTkButton(input_frame, text="Send", command=self.send_prompt)
        self.send_button.pack(side="right", padx=(5, 0))

        # Frame for the bottom row
        bot_frame = ctk.CTkFrame(self)
        bot_frame.pack(side="bottom", fill="x")

        # Add a greeting label at the bottom and center it
        self.greeting_label = ctk.CTkLabel(bot_frame, text="Powered by GroqCloud")
        self.greeting_label.pack(pady=(10, 10), side="bottom")

        # Clear button to clear the conversation area
        self.clear_button = ctk.CTkButton(self, text="Clear", command=self.clear_conversation, fg_color="red", width=80)  # Set width for size
        self.clear_button.pack(side="right", padx=12, pady=10)

        self.user_input.bind("<Return>", self.send_prompt)
        self.bind("<Control-BackSpace>", self.clear_conversation)

        # Set default assistant type
        self.selected_assistant = "General Assistant"

    def update_prompt(self, selected_value):
        self.selected_assistant = selected_value

    def send_prompt(self, event=None):
        user_input = self.user_input.get()
        if user_input:
            self.conversation_area.configure(state="normal")
            # Format for user input
            self.conversation_area.insert("end", "User\n" + user_input + "\n\n")
            self.conversation_area.configure(state="disabled")
            self.user_input.delete(0, "end")
            
            try:
                # Get the system prompt based on selected assistant type
                system_prompt = get_system_prompt(self.selected_assistant)

                # Make a chat completion request with the system prompt and user's input
                chat_completion = client.chat.completions.create(
                    messages=[
                        system_prompt,
                        {
                            "role": "user",
                            "content": user_input,
                        }
                    ],
                    model="llama3-8b-8192",
                )

                # Print the response from the language model
                ai_response = chat_completion.choices[0].message.content
                self.conversation_area.configure(state="normal")
                # Format for AI response
                self.conversation_area.insert("end", f"{self.selected_assistant}\n{ai_response}\n\n")
                self.conversation_area.configure(state="disabled")
                self.conversation_area.see("end")
            except Exception as e:
                self.conversation_area.configure(state="normal")
                self.conversation_area.insert("end", f"{self.selected_assistant}\nCan't connect to Server. API Issue. {e}\n\n")
                self.conversation_area.configure(state="disabled")
                self.conversation_area.see("end")
        

    def clear_conversation(self, event=None):
        self.conversation_area.configure(state="normal")
        self.conversation_area.delete("1.0", "end")  # Clear all text
        self.conversation_area.configure(state="disabled")

# Run the application
if __name__ == "__main__":
    app = ChatbotApp()
    app.mainloop()
