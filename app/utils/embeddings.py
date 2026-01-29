"""Convert text to numbers (embeddings)"""
from sentence_transformers import SentenceTransformer

class EmbeddingManager:
    """Turn text into vectors"""
    
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        """Load model"""
        self.model = SentenceTransformer(model_name)
    
    def get_embedding(self, text):
        """Convert text to vector"""
        embedding = self.model.encode(text, convert_to_tensor=False)
        return embedding.tolist()
