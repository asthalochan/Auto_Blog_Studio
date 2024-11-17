import requests
import time

class TelegramBot:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def send_message(self, message):
        """
        Send a message to the Telegram chat.

        Parameters:
        - message (str): The message to send.

        Returns:
        - bool: True if the message was sent successfully, False otherwise.
        """
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = {"chat_id": self.chat_id, "text": message}
        response = requests.post(url, json=data)
        return response.status_code == 200

    def send_options(self, top_topics):
        """
        Send options for the top topics as inline buttons.

        Parameters:
        - top_topics (list): List of topics to display as options.
        """
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        # Define options as inline buttons
        options = []
        for idx, topic in enumerate(top_topics, start=1):
            options.append([{"text": f"Topic {idx}", "callback_data": f"Topic {idx}"}])

        # Message with inline buttons
        data = {
            "chat_id": self.chat_id,
            "text": "\n\n".join([f"Topic {idx}: {topic[0]}" for idx, topic in enumerate(top_topics, start=1)]),
            "reply_markup": {"inline_keyboard": options}
        }

        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Options sent successfully.")
        else:
            print("Failed to send options:", response.text)

    def clear_old_updates(self):
        """
        Clear old updates to avoid processing outdated messages.
        """
        url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"
        response = requests.get(url)
        data = response.json()

        if data["ok"] and "result" in data and len(data["result"]) > 0:
            last_update_id = data["result"][-1]["update_id"]
            requests.get(f"{url}?offset={last_update_id + 1}")
        else:
            print("No old updates to clear.")

    def get_user_selected_option(self, timeout=600):
        """
        Wait for the user's topic selection via Telegram.

        Parameters:
        - timeout (int): Timeout in seconds to wait for the user's response.

        Returns:
        - str: The callback data of the selected option, or None if no selection is made.
        """
        url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"
        last_update_id = None
        start_time = time.time()

        while time.time() - start_time < timeout:  # Wait for the specified timeout
            response = requests.get(url)
            data = response.json()

            if data["ok"] and "result" in data:
                for update in data["result"]:
                    # Skip already processed updates
                    if update["update_id"] == last_update_id:
                        continue
                    last_update_id = update["update_id"]

                    # Check if there's a callback query (user clicked a button)
                    if "callback_query" in update:
                        callback_data = update["callback_query"]["data"]
                        self.send_message(f"You selected: {callback_data}")
                        return callback_data
            time.sleep(2)  # Check every 2 seconds

        self.send_message("No selection was made within the time limit. Proceeding with Topic 1.")
        return "Topic 1"

if __name__ == "__main__":
    # Replace with your actual bot token and chat ID
    BOT_TOKEN = "your_telegram_bot_token_here"
    CHAT_ID = "your_chat_id_here"

    # Simulated topics
    top_topics = [
        ["AI in Healthcare"],
        ["Machine Learning Basics"],
        ["Data Science Trends 2024"],
        ["NVIDIA AI Research"],
        ["DevOps and AI Integration"]
    ]

    bot = TelegramBot(bot_token=BOT_TOKEN, chat_id=CHAT_ID)

    # Clear old updates
    bot.clear_old_updates()

    # Send options to the user
    bot.send_options(top_topics)

    # Get user's selected option
    selected_option = bot.get_user_selected_option()
    print(f"User selected: {selected_option}")
