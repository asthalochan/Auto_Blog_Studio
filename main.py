import json
from data_preparation import gather_and_save_articles
from embedding_model import generate_embeddings, cluster_topics, rank_topics
from blog_generation import (
    generate_blog_with_references,
    generate_title,
    generate_trending_tags,
    generate_image_prompt,
)
from telegram_integration import TelegramBot
from s3_manager import S3Manager
from medium_integration import MediumIntegration
from blogger_integration import BloggerIntegration

def main():
    # Configuration for each service
    TELEGRAM_BOT_TOKEN = "your_telegram_bot_token_here"
    TELEGRAM_CHAT_ID = "your_chat_id_here"

    AWS_ACCESS_KEY_ID = "your_aws_access_key_id_here"
    AWS_SECRET_ACCESS_KEY = "your_aws_secret_access_key_here"
    AWS_REGION_NAME = "your_aws_region_here"
    S3_BUCKET_NAME = "your_bucket_name_here"
    S3_TOKEN_PATH = "refresh_token.txt"

    MEDIUM_INTEGRATION_TOKEN = "your_medium_integration_token_here"

    GOOGLE_CLIENT_ID = "your_google_client_id_here"
    GOOGLE_CLIENT_SECRET = "your_google_client_secret_here"
    GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"
    GOOGLE_REFRESH_TOKEN = "your_google_refresh_token_here"
    BLOGGER_BLOG_ID = "your_blogger_blog_id_here"

    # Initialize integrations
    telegram = TelegramBot(bot_token=TELEGRAM_BOT_TOKEN, chat_id=TELEGRAM_CHAT_ID)
    s3_manager = S3Manager(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME,
        bucket_name=S3_BUCKET_NAME,
    )
    medium = MediumIntegration(integration_token=MEDIUM_INTEGRATION_TOKEN)
    blogger = BloggerIntegration(
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/blogger"],
        token_uri=GOOGLE_TOKEN_URI,
        refresh_token=GOOGLE_REFRESH_TOKEN,
        blog_id=BLOGGER_BLOG_ID,
    )

    # Step 1: Gather articles and save them
    telegram.send_message("Starting the blog generation process... 📝")
    saved_file_path = gather_and_save_articles()
    if not saved_file_path:
        telegram.send_message("Failed to gather articles. Exiting process.")
        return

    # Step 2: Load saved articles
    try:
        with open(saved_file_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        telegram.send_message(f"Error loading articles: {e}")
        return

    telegram.send_message("Articles gathered successfully! 📑")

    # Step 3: Generate embeddings and cluster topics
    embeddings, topics = generate_embeddings(data)
    if not embeddings:
        telegram.send_message("No embeddings generated. Exiting process.")
        return

    clustered_topics = cluster_topics(embeddings, topics)
    top_topics = rank_topics(clustered_topics)

    # Step 4: Send top topics to Telegram and get user selection
    telegram.send_options(top_topics)
    selected_option = telegram.get_user_selected_option()

    selected_topic_idx = int(selected_option.split()[-1]) - 1
    if selected_topic_idx < 0 or selected_topic_idx >= len(top_topics):
        telegram.send_message("Invalid selection. Proceeding with the first topic.")
        selected_topic_idx = 0

    selected_topic = top_topics[selected_topic_idx][0]
    telegram.send_message(f"Selected topic: {selected_topic}")

    # Step 5: Generate the blog
    blog_post = generate_blog_with_references(selected_topic, data)
    if not blog_post:
        telegram.send_message("Blog generation failed. Exiting process.")
        return

    # Step 6: Generate title, tags, and image prompt
    title = generate_title(blog_post)
    tags = generate_trending_tags(blog_post)
    image_prompt = generate_image_prompt(blog_post)

    # Step 7: Generate the image (e.g., using Stable Diffusion)
    telegram.send_message("Generating the image for the blog... 🎨")
    from diffusers import StableDiffusionPipeline
    import torch

    model_id = "CompVis/stable-diffusion-v1-4"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")

    width, height = 768, 512
    image = pipe(prompt=image_prompt, height=height, width=width).images[0]
    image.save("generated_image.png")

    telegram.send_message("Image generated successfully! 🖼️")

    # Step 8: Publish to Medium
    user_id = medium.get_user_id()
    if user_id:
        medium_response = medium.create_medium_post(
            user_id, title, blog_post, content_format="html", tags=tags
        )
        if medium_response:
            telegram.send_message(f"Blog successfully posted on Medium! 🚀\nURL: {medium_response['data']['url']}")
        else:
            telegram.send_message("Failed to post blog on Medium.")

    # Step 9: Publish to Blogger
    credentials = blogger.get_credentials()
    if credentials:
        blogger_response = blogger.create_blog_post(title, blog_post)
        if blogger_response:
            telegram.send_message(f"Blog successfully posted on Blogger! 📝\nURL: {blogger_response['url']}")
        else:
            telegram.send_message("Failed to post blog on Blogger.")

    # Step 10: Completion message
    telegram.send_message("All processes completed successfully! 🎉")

if __name__ == "__main__":
    main()
