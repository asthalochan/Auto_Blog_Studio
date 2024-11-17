def generate_blog_with_references(top_topic, data):
    """
    Generate a detailed blog post based on a selected topic and associated content.

    Parameters:
    - top_topic (str): The selected topic for the blog.
    - data (dict): Articles data with content.

    Returns:
    - blog_post (str): The generated blog post.
    """
    # Retrieve content associated with the top topic
    def get_content_for_topic(data, topic):
        for publication, articles in data.items():
            for article in articles:
                if article.get("main_topic") == topic:
                    return article.get("content", "")
        return ""

    topic_content = get_content_for_topic(data, top_topic)
    if not topic_content:
        print(f"No content found for topic: {top_topic}")
        return None

    # Define the prompt for generating the blog post
    system_message = (
        "You will be given a topic title and content to reference. Write a detailed and engaging blog post based on this material. "
        "Begin with an introduction that hooks the reader and provides an overview of the topic. Break the main content into clear, well-organized sections, "
        "each exploring a key aspect or subtopic from the reference content. Add any relevant examples, actionable tips, or recent data to enrich the post. "
        "Write in a friendly, conversational tone and aim for a length of about 1,000-1,200 words. Conclude with a summary of the key points and a call-to-action "
        "that encourages readers to engage further, such as by sharing their thoughts or exploring related resources."
    )

    question = f"Write blog with this Reference Topic: {top_topic}.\n Content: {topic_content[:650]}..."
    prompt = (
        "<|begin_of_text|>"
        "<|start_header_id|>system<|end_header_id|>"
        f"{system_message}"
        "<|eot_id|>"
        "<|start_header_id|>user<|end_header_id|>"
        f"{question}"
        "<|eot_id|>"
        "<|start_header_id|>assistant<|end_header_id|>"
    )

    # Use LLM API for blog generation
    blog_post = llama(prompt_or_messages=prompt, max_tokens=4096, temperature=0.6)

    # Second LLM pass for content refinement
    refinement_prompt = (
        f"Refine the following blog post for better readability, coherence, and completeness. Remove redundancy, ensure all sentences are complete, "
        f"and make it concise without losing important details. The output format should include headings as HTML-like tags (e.g., <h1>, <h2>). "
        f"Blog Post: \n {blog_post}"
    )
    refined_blog_post = llama(prompt_or_messages={"role": "user", "content": refinement_prompt}, max_tokens=4096, temperature=0.6)
    return refined_blog_post

def generate_title(topic_content):
    """
    Generate an SEO-friendly title for the blog post.

    Parameters:
    - topic_content (str): Content related to the blog topic.

    Returns:
    - title (str): Generated title.
    """
    title_prompt = (
        "Create an engaging, SEO-friendly title that captures the core message of the following content. "
        "Make it attention-grabbing and concise to appeal to online readers and maximize search visibility. "
        f"Content: '{topic_content[:500]}...'"
    )
    title_response = llama(prompt_or_messages={"role": "user", "content": title_prompt}, max_tokens=20, temperature=0.9)
    return title_response.strip()

def generate_trending_tags(topic_content):
    """
    Generate trending tags for the blog post.

    Parameters:
    - topic_content (str): Content related to the blog topic.

    Returns:
    - tags (list): List of relevant tags.
    """
    tags_prompt = (
        "Based on the following content, generate 5 trending, common, and relevant tags that capture key aspects of the topic. "
        "Return the tags as a comma-separated list. "
        f"Content: '{topic_content[:500]}...'"
    )
    tags_response = llama(prompt_or_messages={"role": "user", "content": tags_prompt}, max_tokens=20, temperature=0.9)
    return [tag.strip() for tag in tags_response.split(",") if tag.strip()]

def generate_image_prompt(topic_content):
    """
    Generate a realistic image prompt based on the blog content.

    Parameters:
    - topic_content (str): Content related to the blog topic.

    Returns:
    - image_prompt (str): Generated image prompt.
    """
    image_prompt_instructions = (
        "Using the following content, create a realistic and visually descriptive prompt for generating an image suitable for a blog post. "
        "The prompt should describe the scene with natural, true-to-life details, focusing on accurate colors, textures, and settings. "
        "Avoid abstract or overly stylized descriptions. "
        f"Content: '{topic_content[:500]}...'"
    )
    image_prompt_response = llama(prompt_or_messages={"role": "user", "content": image_prompt_instructions}, max_tokens=60, temperature=0.8)
    return image_prompt_response.strip()

if __name__ == "__main__":
    # Example usage
    simulated_data = {
        "Towards Data Science": [
            {"main_topic": "AI in Healthcare", "content": "Some detailed content about AI in healthcare..."},
        ]
    }
    top_topic = "AI in Healthcare"

    # Generate blog
    refined_blog = generate_blog_with_references(top_topic, simulated_data)
    print(f"Generated Blog:\n{refined_blog}")

    # Generate title
    title = generate_title(refined_blog)
    print(f"Generated Title: {title}")

    # Generate tags
    tags = generate_trending_tags(refined_blog)
    print(f"Generated Tags: {tags}")

    # Generate image prompt
    image_prompt = generate_image_prompt(refined_blog)
    print(f"Generated Image Prompt: {image_prompt}")
