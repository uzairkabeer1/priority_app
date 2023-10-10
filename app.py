from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

try:
    with open('priority_words.pkl', 'rb') as f:
        priority_words = pickle.load(f)
except Exception as e:
    app.logger.error("Error loading priority_words.pkl: %s", e)
    priority_words = {}

def get_priority(description):
    try:
        for priority, words in priority_words.items():
            if any(word in description.lower() for word in words):
                return priority
    except Exception as e:
        app.logger.error("Error determining priority: %s", e)
    return 'low'  

@app.route('/get_priority', methods=['POST'])
def add_task():
    try:
        task_description = request.form.get('title')
        priority = get_priority(task_description)
        task = {'title': task_description, 'priority': priority}
        return jsonify(task)
    except Exception as e:
        app.logger.error("Error processing request: %s", e)
        return jsonify({"error": "Failed to process request"}), 500

if __name__ == '__main__':
    app.run(debug=True)
