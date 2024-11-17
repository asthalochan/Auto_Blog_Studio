from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

class BloggerIntegration:
    def __init__(self, client_id, client_secret, scopes, token_uri, refresh_token, blog_id):
        """
        Initialize BloggerIntegration.

        Parameters:
        - client_id (str): Google Client ID.
        - client_secret (str): Google Client Secret.
        - scopes (list): Google API scopes.
        - token_uri (str): Google token URI.
        - refresh_token (str): Refresh token for authentication.
        - blog_id (str): Blogger Blog ID.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        self.token_uri = token_uri
        self.refresh_token = refresh_token
        self.blog_id = blog_id
        self.credentials = None

    def get_credentials(self):
        """
        Obtain valid Google API credentials using the refresh token.

        Returns:
        - Credentials: Google API credentials if successful, None otherwise.
        """
        try:
            self.credentials = Credentials(
                None,
                refresh_token=self.refresh_token,
                client_id=self.client_id,
                client_secret=self.client_secret,
                token_uri=self.token_uri,
                scopes=self.scopes
            )

            if not self.credentials.valid:
                self.credentials.refresh(Request())
            return self.credentials
        except Exception as e:
            print(f"Error refreshing credentials: {e}")
            return None

    def create_blog_post(self, title, content):
        """
        Create a blog post on Blogger.

        Parameters:
        - title (str): Title of the blog post.
        - content (str): HTML content of the blog post.

        Returns:
        - dict: Response JSON from Blogger API if successful, None otherwise.
        """
        if not self.credentials:
            print("Credentials are not valid. Unable to create post.")
            return None

        try:
            service = build("blogger", "v3", credentials=self.credentials)
            post = {
                "title": title,
                "content": content
            }

            result = service.posts().insert(blogId=self.blog_id, body=post).execute()
            print(f"Blog post published successfully! URL: {result['url']}")
            return result
        except Exception as e:
            print(f"Error creating blog post: {e}")
            return None

if __name__ == "__main__":
    # Replace with your actual Google credentials and blog details
    CLIENT_ID = "your_google_client_id_here"
    CLIENT_SECRET = "your_google_client_secret_here"
    SCOPES = ["https://www.googleapis.com/auth/blogger"]
    TOKEN_URI = "https://oauth2.googleapis.com/token"
    REFRESH_TOKEN = "your_refresh_token_here"
    BLOG_ID = "your_blog_id_here"

    # Initialize BloggerIntegration
    blogger = BloggerIntegration(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=SCOPES,
        token_uri=TOKEN_URI,
        refresh_token=REFRESH_TOKEN,
        blog_id=BLOG_ID
    )

    # Get credentials
    credentials = blogger.get_credentials()
    if not credentials:
        print("Failed to authenticate with Google API.")
        exit()

    # Example blog data
    title = "Exploring AI in Healthcare"
    content = "<h1>Exploring AI in Healthcare</h1><p>AI is transforming healthcare...</p>"

    # Create a new blog post
    response = blogger.create_blog_post(title, content)
    if response:
        print(f"Post URL: {response['url']}")
    else:
        print("Failed to create blog post.")
