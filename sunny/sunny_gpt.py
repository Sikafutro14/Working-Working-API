import openai
from tkinter import messagebox

class ApplicationTrackerGPT:
    def __init__(self, app):
        self.api_key = app.api_key  # Ensure API key is correctly referenced
        self.client = None
        self.app = app
    
    def initialize_openai_client(self):
        try:
            openai.api_key = self.api_key  # Set the API key for OpenAI
            self.client = openai
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize OpenAI client: {e}")

    def ask_chatgpt(self):
        if not self.client:
            messagebox.showerror("Error", "OpenAI client is not initialized.")
            return

        prompt = self.app.prompt_entry.get()
        if not prompt.strip():
            messagebox.showwarning("Input Error", "Prompt cannot be empty.")
            return

        try:
            response = self.client.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150
            )
            response_text = response['choices'][0]['message']['content'].strip()

            # Update the response box in the app
            self.app.response_box.configure(state="normal")
            self.app.response_box.insert("end", f"You: {prompt}\n\nChatGPT: {response_text}\n\n")
            self.app.response_box.configure(state="disabled")
            self.app.response_box.see("end")
            self.app.prompt_entry.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get a response from ChatGPT: {e}")

