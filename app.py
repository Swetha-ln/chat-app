from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

def load_documentation():
    documentation = {}
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as file:
                documentation[filename.replace('.txt', '')] = file.read()
    return documentation

documentation = load_documentation()

def search_documentation(query, cdp_name):
    if cdp_name not in documentation:
        return "Documentation not found for this CDP."
    
    keywords = query.lower().split()
    relevant_sections = []
    for line in documentation[cdp_name].split('\n'):
        if any(keyword in line.lower() for keyword in keywords):
            relevant_sections.append(line)
    
    if not relevant_sections:
        return "No relevant information found."
    
    return "\n".join(relevant_sections)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    query = data.get('query')
    cdp_name = data.get('cdp')
    
    if not query or not cdp_name:
        return jsonify({'response': 'Please provide a query and CDP name.'})
    
    response = search_documentation(query, cdp_name)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)