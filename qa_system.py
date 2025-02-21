import logging
from sentence_transformers import SentenceTransformer

class QuestionAnswering:
    def __init__(self, vector_db):
       
        self.vector_db = vector_db
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Use a pre-trained model
        logging.info("Initialized QuestionAnswering system.")

    def answer(self, question):
      
        # Retrieve relevant text chunks based on the query
        relevant_chunks = self.vector_db.retrieve(question)

        if not relevant_chunks:
            return f"Q: {question}\nA:couldn't find relevant information."

        # Combine the retrieved chunks for response generation
        context = " ".join(relevant_chunks)

        # Try to extract the answer from the context (simple approach here)
        response = self.extract_answer_from_context(context, question)

        return f"Q: {question}\nA: {response}"

    def extract_answer_from_context(self, context, question):
      
        # A more sophisticated method for extracting an answer
        sentences = context.split('. ')
        # Look for a sentence that most directly addresses the question
        relevant_sentence = None
        for sentence in sentences:
            if self.is_relevant_sentence(sentence, question):
                relevant_sentence = sentence
                break
        
       
        if relevant_sentence is None:
            relevant_sentence = sentences[0]
        
        return relevant_sentence.strip() + '.'

    def is_relevant_sentence(self, sentence, question):
     
        return any(keyword.lower() in sentence.lower() for keyword in question.split())

