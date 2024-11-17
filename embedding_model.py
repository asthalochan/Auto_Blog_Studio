from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import numpy as np

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(data):
    """
    Generate embeddings for the main topics in the data.

    Parameters:
    - data (dict): Articles data with main topics.

    Returns:
    - embeddings (list): List of generated embeddings.
    - topics (list): Corresponding main topics.
    """
    embeddings = []
    topics = []
    for publication, articles in data.items():
        for article in articles:
            main_topic = article.get("main_topic")
            if main_topic and "Error" not in main_topic:
                embedding = model.encode(main_topic)
                embeddings.append(embedding)
                topics.append(main_topic)
    return embeddings, topics

def cluster_topics(embeddings, topics, num_clusters=3):
    """
    Cluster topics using KMeans clustering.

    Parameters:
    - embeddings (list): List of topic embeddings.
    - topics (list): Corresponding topics for embeddings.
    - num_clusters (int): Number of clusters.

    Returns:
    - clustered_topics (dict): Topics organized by cluster labels.
    """
    if len(embeddings) == 0:
        print("No embeddings provided for clustering.")
        return {}

    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    labels = kmeans.fit_predict(embeddings)

    clustered_topics = {i: [] for i in range(num_clusters)}
    for idx, label in enumerate(labels):
        clustered_topics[label].append(topics[idx])

    return clustered_topics

def rank_topics(clustered_topics):
    """
    Rank topics based on a simulated relevance score.

    Parameters:
    - clustered_topics (dict): Topics organized by cluster labels.

    Returns:
    - top_topics (list): List of top-ranked topics.
    """
    import random

    topic_scores = []
    for cluster, topic_list in clustered_topics.items():
        for topic in topic_list:
            relevance_score = random.uniform(0, 1)  # Simulate a relevance score
            topic_scores.append((topic, relevance_score))

    # Sort by relevance score in descending order
    topic_scores = sorted(topic_scores, key=lambda x: x[1], reverse=True)
    return topic_scores[:5]  # Top 5 topics

if __name__ == "__main__":
    # Example usage
    # Simulate loaded JSON data
    data = {
        "Towards Data Science": [
            {"main_topic": "AI in Healthcare", "content": "Some content..."},
            {"main_topic": "Data Science Trends 2024", "content": "Some content..."}
        ],
        "Dev.to": [
            {"main_topic": "Machine Learning Basics", "content": "Some content..."}
        ]
    }

    # Generate embeddings
    embeddings, topics = generate_embeddings(data)

    # Cluster topics
    clustered_topics = cluster_topics(embeddings, topics, num_clusters=3)

    # Rank topics
    top_topics = rank_topics(clustered_topics)

    # Print top topics
    print("Top Topics:")
    for idx, (topic, score) in enumerate(top_topics, 1):
        print(f"Top {idx} Topic: '{topic}' with relevance score {score:.2f}")
