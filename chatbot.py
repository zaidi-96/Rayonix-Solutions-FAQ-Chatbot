import json
import re

class SoftwareBusinessChatbot:
    def __init__(self, faq_file='faq.json'):
        """
        Initialize the chatbot by loading the FAQ knowledge base.
        """
        self.faq_file = faq_file
        self.faqs = self.load_faqs()
        self.exit_commands = {"bye", "goodbye", "exit", "quit", "see you"}

    def load_faqs(self):
        """
        Load questions and answers from the JSON file.
        """
        try:
            with open(self.faq_file, 'r') as file:
                data = json.load(file)
            return data['faqs']
        except FileNotFoundError:
            print(f"Error: The file {self.faq_file} was not found.")
            return []
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from {self.faq_file}.")
            return []

    def preprocess_text(self, text):
        """
        Clean and preprocess the user's input text.
        Converts to lowercase and removes punctuation.
        """
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text) # Remove punctuation
        return text

    def find_best_match(self, user_input):
        """
        Find the best matching FAQ based on keyword frequency in the user's input.
        Returns the matching FAQ entry or None.
        """
        processed_input = self.preprocess_text(user_input)
        words = set(processed_input.split())
        
        best_match = None
        highest_score = 0

        for faq in self.faqs:
            score = len(words.intersection(faq['keywords']))
            if score > highest_score:
                highest_score = score
                best_match = faq

        # Only return a match if at least one keyword was found
        return best_match if highest_score > 0 else None

    def ask_clarification(self, vague_input):
        """
        Handles vague inputs by asking a clarifying question.
        """
        vague_input = vague_input.lower()
        if 'app' in vague_input:
            return "I see you're interested in an app. Do you need a mobile, web, or desktop solution?"
        elif 'cost' in vague_input or 'price' in vague_input:
            return "I'd be happy to discuss pricing. Could you tell me a bit more about your project type (e.g., website, mobile app, custom software)?"
        else:
            return "That's an interesting question. Can you tell me a bit more about what you're looking for?"

    def start_chat(self):
        """
        Main method to run the chatbot interaction loop.
        """
        print("\n=== Welcome to the Rayonix Solutions Chatbot ===")
        print("I'm here to answer your questions about our services.")
        print("You can ask me about pricing, services, or how to get started.")
        print("Type 'bye' at any time to exit.\n")

        while True:
            user_input = input("You: ").strip()

            # Check for exit commands
            if user_input.lower() in self.exit_commands:
                print(f"Chatbot: {self.get_fallback_response('exit')}")
                break

            # Check for greetings
            if self.find_best_match(user_input) and self.find_best_match(user_input)['question'] == 'Greeting':
                print(f"Chatbot: {self.find_best_match(user_input)['answer']}")
                continue

            # Try to find a match in the FAQs
            match = self.find_best_match(user_input)

            if match:
                print(f"Chatbot: {match['answer']}")
            else:
                # If no match, ask for clarification
                clarification = self.ask_clarification(user_input)
                print(f"Chatbot: {clarification}")

    def get_fallback_response(self, context):
        """
        Provides a context-aware fallback response.
        """
        for faq in self.faqs:
            if faq['question'] == context.capitalize():
                return faq['answer']
        return "I'm not sure how to handle that. Please try asking something else."

# Run the chatbot
if __name__ == "__main__":
    bot = SoftwareBusinessChatbot()
    bot.start_chat()