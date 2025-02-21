import os
import logging
from data_ingestion import fetch_and_preprocess_content
from vector_db import VectorDatabase
from qa_system import QuestionAnswering
from concurrent.futures import ThreadPoolExecutor

# Configurations
URL = "https://www2.deloitte.com/us/en/insights/economy/global-economic-outlook/weekly-update/weekly-update-2023-10.html?icid=archive_click"
QUESTION_FILE = "questions.txt"
OUTPUT_FILE = "responses.txt"
CACHED_CONTENT_FILE = "cached_content.txt"

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    logging.info("Starting Economic Update QA System...")

    # Step 1: Fetch and clean data (with cache check)
    content = load_or_fetch_content()
    if not content:
        logging.error("Failed to fetch or load content.")
        return

    # Step 2: Store embeddings in vector database
    logging.info("Initializing vector database and storing embeddings...")
    vectordb = VectorDatabase()  # Vector database using SentenceTransformer
    vectordb.store(content)

    # Step 3: Initialize the QA system
    qa_system = QuestionAnswering(vectordb)

    # Step 4: Read user queries
    questions = load_questions()
    if not questions:
        logging.error(f"Error: {QUESTION_FILE} not found or empty.")
        return

    logging.info(f"Processing {len(questions)} questions...")

    # Step 5: Generate responses (parallelize question answering)
    responses = process_questions_in_parallel(qa_system, questions)

    # Step 6: Save responses to file
    save_responses(responses)

def load_or_fetch_content():
  
    if os.path.exists(CACHED_CONTENT_FILE):
        logging.info("Loading content from cache...")
        with open(CACHED_CONTENT_FILE, "r", encoding="utf-8") as f:
            return f.read()
    else:
        logging.info("Fetching and processing Deloitte economic info .")
        try:
            content = fetch_and_preprocess_content(URL)
            with open(CACHED_CONTENT_FILE, "w", encoding="utf-8") as f:
                f.write(content)
            return content
        except Exception as e:
            logging.error(f"Failed to fetch content: {e}")
            return None

def load_questions():
  
    if not os.path.exists(QUESTION_FILE):
        logging.error(f"Error: {QUESTION_FILE} not found.")
        return []
    
    try:
        with open(QUESTION_FILE, "r", encoding="utf-8") as file:
            questions = [line.strip() for line in file.readlines() if line.strip()]
        return questions
    except Exception as e:
        logging.error(f"Error reading {QUESTION_FILE}: {e}")
        return []

def process_questions_in_parallel(qa_system, questions):
   
    def process_question(q):
        return qa_system.answer(q)

    with ThreadPoolExecutor() as executor:
        responses = list(executor.map(process_question, questions))
    return responses

def save_responses(responses):

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            for response in responses:
                file.write(response + "\n")
        logging.info(f"Responses saved to {OUTPUT_FILE}")
    except Exception as e:
        logging.error(f"Error saving responses: {e}")

if __name__ == "__main__":
    main()
