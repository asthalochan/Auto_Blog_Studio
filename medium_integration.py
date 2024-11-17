import requests
import json

class MediumIntegration:
    def __init__(self, integration_token):
        """
        Initialize the MediumIntegration.

        Parameters:
        - integration_token (str): Medium integration token.
        """
        self.integration_token = integration_token
        self.base_url = "https://api.medium.com/v1"

    def get_user_id(self):
        """
        Fetch the user ID associated with the Medium integration token.

        Returns:
        - str: The user ID if successful, None otherwise.
        """
        url = f"{self.base_url}/me"
        headers = {"Authorization": f"Bearer {self.integration_token}"}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            user_info = response.json()
            return user_info.get('data', {}).get('id')
        except Exception as e:
            print(f"Error fetching user information: {e}")
            return None

    def create_medium_post(self, user_id, title, content, content_format='html', tags=None, publish_status='public'):
        """
        Create a new post on Medium.

        Parameters:
        - user_id (str): Medium user ID.
        - title (str): The title of the post.
        - content (str): The content of the post in the specified format.
        - content_format (str): Format of the content ('html' or 'markdown').
        - tags (list): List of tags for the post.
        - publish_status (str): Publishing status ('public', 'draft', or 'unlisted').

        Returns:
        - dict: Response JSON if successful, None otherwise.
        """
        url = f"{self.base_url}/users/{user_id}/posts"
        headers = {
            "Authorization": f"Bearer {self.integration_token}",
            "Content-Type": "application/json"
        }

        data = {
            "title": title,
            "contentFormat": content_format,
            "content": content,
            "tags": tags or [],
            "publishStatus": publish_status
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error creating Medium post: {e}")
            return None


if __name__ == "__main__":
    # Replace with your actual Medium integration token
    MEDIUM_INTEGRATION_TOKEN = "your_medium_integration_token_here"

    # Initialize MediumIntegration
    medium = MediumIntegration(integration_token=MEDIUM_INTEGRATION_TOKEN)

    # Get user ID
    user_id = medium.get_user_id()
    if not user_id:
        print("Failed to retrieve Medium user ID.")
        exit()

    # Example post data
    title = "Exploring AI in Healthcare"
    content = "<h1>Exploring AI in Healthcare</h1><p>AI is transforming healthcare...</p>"
    tags = ["AI", "Healthcare", "Technology"]
    publish_status = "public"  # Options: 'public', 'draft', 'unlisted'

    # Create a new post
    response = medium.create_medium_post(user_id, title, content, content_format="html", tags=tags, publish_status=publish_status)
    if response:
        print(f"Post published successfully! URL: {response['data']['url']}")
    else:
        print("Failed to publish post.")
