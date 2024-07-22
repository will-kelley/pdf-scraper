import os
import re
import fitz 
from flask import Flask, request, jsonify, render_template
from datetime import datetime
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

#Date pattern for current samples (change as needed)
DATE_PATTERN = r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})\b'

def extract_text_from_pdfs(directory):
    pdf_texts = {}
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            text = ""
            try:
                with fitz.open(file_path) as pdf:
                    for page in pdf:
                        text += page.get_text()
                pdf_texts[filename] = text.replace('\n', ' ').replace('\r', '')
                logging.info(f"Successfully processed {filename}")
            except Exception as e:
                logging.error(f"Error processing {filename}: {e}")
    return pdf_texts

def find_dates(text):
    dates = re.findall(DATE_PATTERN, text)
    parsed_dates = []
    for date_str in dates:
        for fmt in ('%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d', '%Y/%m/%d'):
            try:
                parsed_dates.append(datetime.strptime(date_str, fmt))
                break
            except ValueError:
                continue
    return parsed_dates

def calculate_relevance_score(text, query):
    words = text.lower().split()
    query_words = query.lower().split()
    score = 0
    for query_word in query_words:
        if query_word in words:
            score += words.count(query_word)
    return score

def get_most_recent_date(text):
    dates = find_dates(text)
    return max(dates) if dates else None

def extract_relevant_sentences(text, query):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    query_words = query.lower().split()
    relevant_sentences = [sentence.strip() for sentence in sentences if any(query_word in sentence.lower() for query_word in query_words)]
    return '. '.join(relevant_sentences) + '.'

pdf_directory = "./pdfs"
pdf_texts = extract_text_from_pdfs(pdf_directory)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_pdfs():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is missing"}), 400
    
    results = []
    for filename, text in pdf_texts.items():
        score = calculate_relevance_score(text, query)
        recent_date = get_most_recent_date(text)
        if score > 0:
            relevant_text = extract_relevant_sentences(text, query)
            results.append({"filename": filename, "score": score, "recent_date": recent_date, "text": relevant_text})
    
    #Sorting by score/date
    results = sorted(results, key=lambda x: (x["score"], x["recent_date"] or datetime.min), reverse=True)
    
    if not results:
        return jsonify({"message": "No matches found"}), 404
    
    #Formatting
    formatted_results = {result["filename"]: result["text"] for result in results}
    
    return jsonify(formatted_results), 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == '__main__':
    app.run(debug=True)
