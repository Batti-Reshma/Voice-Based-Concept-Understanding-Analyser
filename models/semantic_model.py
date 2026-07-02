from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the Sentence-BERT model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(reference_text, user_text):
    """
    Calculate semantic similarity between
    the reference concept and the user's explanation.
    """

    embeddings = model.encode([reference_text, user_text])

    similarity = cosine_similarity(
         [embeddings[0]],
         [embeddings[1]]
    )[0][0]

    # Convert -1..1 to 0..100
    similarity = max(0, similarity) * 100

    return round(float(similarity), 2)