from flask import Flask, request, render_template, jsonify
import requests
from xml.etree import ElementTree
from answer import answer_question  # Import the function from answer.py

app = Flask(__name__)

history = []
MAX_HISTORY_LENGTH = 2  # Limit history to 5 items

# Function to get articles from PubMed
def get_article_from_pubmed(query, start=0):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "xml",
        "retstart": start,  # Start point for the next set of results
        "retmax": 5  # Number of results
    }
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        # Parse the XML response to get the list of PMIDs
        root = ElementTree.fromstring(response.text)
        pmids = [id.text for id in root.findall(".//Id")]
        
        if not pmids:
            return "No articles found for your query."
        
        # Fetch article details for each PMID
        articles = []
        for pmid in pmids:
            article_details = fetch_article_details(pmid)
            articles.append(article_details)
        
        return articles
    else:
        return "Could not fetch information from PubMed."

def fetch_article_details(pmid):
    esummary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml"
    }
    response = requests.get(esummary_url, params=params)
    
    if response.status_code == 200:
        # Parse the XML response
        root = ElementTree.fromstring(response.text)
        docsum = root.find(".//DocSum")
        
        # Extract article title and link
        title = docsum.find(".//Item[@Name='Title']").text
        pubmed_link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        
        return {
            "title": title,
            "link": pubmed_link
        }
    else:
        return {"title": "Error", "link": "#"}

@app.route("/", methods=["GET", "POST"])
def home():
    articles = []
    article_query = ""  # Default empty article query
    active_tab = "ask-question"  # Default tab is "Ask Question"
    # history = []  # Initialize an empty history for this session
    
    if request.method == "POST":
        # Handle Question Submission
        question = request.form.get('question')
        article_query = request.form.get('article-query')

        if question:  # If it's a question submission
            answer = answer_question(question)  # Get answer dynamically from the model
            
            # Add the new question and answer to history
            history.append({'question': question, 'answer': answer})
            
            # Ensure history doesn't exceed the maximum length
            if len(history) > MAX_HISTORY_LENGTH:
                history.pop(0)  # Remove the oldest question-answer pair

            active_tab = "ask-question"  # Keep active tab as "Ask Question"
        
        elif article_query:  # If it's an article query
            active_tab = "articles"  # Switch active tab to "Articles"
            articles = get_article_from_pubmed(article_query)  # Get articles based on the query

    return render_template("index.html", history=history, articles=articles, active_tab=active_tab, article_query=article_query)

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get('question')
    # history = []  # Initialize history as an empty list for the API endpoint
    
    if question:
        answer = answer_question(question)  # Get answer from the model
        history.append({'question': question, 'answer': answer})  # Add to history
        
        # Ensure history doesn't exceed the maximum length
        if len(history) > MAX_HISTORY_LENGTH:
            history.pop(0)  # Remove the oldest question-answer pair
        
        articles = get_article_from_pubmed(question)  # Get articles based on the question

        return jsonify({'answer': answer, 'history': history, 'articles': articles})
    return jsonify({'error': 'No question provided.'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
