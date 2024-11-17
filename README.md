Here’s the complete **README.md** file that you can copy and paste:

```markdown
# Automatic Blog Writer

## Overview
The Automatic Blog Writer is a Python-based system that:
1. Gathers articles from popular sources such as Towards Data Science, Dev.to, KDNuggets, and NVIDIA Blog.
2. Clusters and ranks topics using machine learning embeddings and KMeans.
3. Interacts with users via Telegram to choose topics.
4. Automatically generates SEO-friendly blogs, titles, tags, and images using LLMs and Stable Diffusion.
5. Publishes the generated content to Medium and Google Blogger.

---

## Features
- **Content Aggregation**: Fetches articles from RSS feeds and popular websites.
- **Topic Clustering**: Groups related topics using embeddings from Sentence Transformers.
- **Blog Generation**: Creates detailed and engaging blogs based on user-selected topics.
- **Image Generation**: Generates visuals using Stable Diffusion for a polished blog.
- **Publishing**: Posts to Medium and Google Blogger with minimal effort.
- **User Interaction**: Telegram bot interface for seamless topic selection.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- A Medium integration token
- Google Blogger API credentials
- AWS credentials for S3 (for token management)
- A Telegram bot token and chat ID

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/automatic-blog-writer.git
   cd automatic-blog-writer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   Update the tokens and credentials in the respective places within the `main.py` file.

4. Run the script:
   ```bash
   python main.py
   ```

---

## Configuration
Edit the following values in `main.py` to match your setup:

- **Telegram Bot**:
  - `TELEGRAM_BOT_TOKEN`: Token for your Telegram bot.
  - `TELEGRAM_CHAT_ID`: Chat ID for sending updates.

- **AWS S3**:
  - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`: AWS credentials for token management.
  - `AWS_REGION_NAME`, `S3_BUCKET_NAME`: AWS S3 bucket details.

- **Medium API**:
  - `MEDIUM_INTEGRATION_TOKEN`: Your Medium integration token.

- **Google Blogger API**:
  - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`: Credentials for Google API.
  - `BLOGGER_BLOG_ID`: Your Blogger blog ID.

---

## Usage
1. Start the script:
   ```bash
   python main.py
   ```

2. Follow the prompts on Telegram to choose a topic for the blog.

3. The script will:
   - Fetch and process articles.
   - Generate a blog, title, tags, and images.
   - Publish the blog to Medium and Google Blogger.

4. Receive notifications on Telegram for every step.

---

## Project Structure
```
automatic_blog_writer/
│
├── main.py                   # Entry point of the application
├── data_preparation.py       # Fetches and processes articles
├── embedding_model.py        # Embedding generation and clustering
├── blog_generation.py        # Blog and content generation logic
├── telegram_integration.py   # Telegram bot interaction
├── s3_manager.py             # AWS S3 token management
├── medium_integration.py     # Medium API integration
├── blogger_integration.py    # Blogger API integration
├── requirements.txt          # Dependencies
└── README.md                 # Project instructions
```

---



## Contributions
We welcome contributions from the community! Here's how you can help:
1. Fork the repository on GitHub.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request describing your changes.

Please ensure that your contributions are well-documented and tested.

---

## Support
If you encounter any issues, feel free to:
- Open an issue on GitHub with a detailed description of the problem.
- Contact the author via email at [mohantaastha@gmail.com].
- Post your questions in the discussions section of the repository.

---

## Roadmap
- **Multi-Language Support**: Extend blog generation to support multiple languages.
- **Advanced Analytics**: Integrate metrics for analyzing blog performance.
- **Additional Platforms**: Add publishing support for other platforms like WordPress or Substack.
- **UI Dashboard**: Create a user-friendly dashboard for better management.

---

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute the software as per the license terms.

---

## Author
Your Name  
[GitHub Profile](https://github.com/asthalochan)  
[LinkedIn Profile](https://www.linkedin.com/in/asthalochan-mohanta/)  
```

