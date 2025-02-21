import logging
from sentence_transformers import SentenceTransformer
import numpy as np

class VectorDatabase:
    def __init__(self):

        # Initialize the sentence transformer model
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Use a pre-trained model
        self.text_data = []  # Store text data
        self.embeddings = []  # Store embeddings for retrieval

    def store(self, content):
 
        # Split content into chunks (or you can use another approach)
        self.text_data = content.split(". ")
        
        # Encode the chunks into embeddings using the model
        self.embeddings = self.model.encode(self.text_data)

        logging.info(f"Stored {len(self.text_data)} text chunks in retrieval system.")

    def retrieve(self, query, top_k=5):
       
        try:
            # Generate the embedding for the query using the model
            query_embedding = self.model.encode([query])

            # Compute cosine similarity to find the top-k most relevant text chunks
            similarities = np.dot(self.embeddings, query_embedding.T).flatten()
            top_k_indices = similarities.argsort()[-top_k:][::-1]

            # Retrieve the top-k closest text chunks
            relevant_texts = [self.text_data[i] for i in top_k_indices]

            return relevant_texts

        except Exception as e:
            logging.error(f"Error retrieving text chunks: {e}")
            return []
