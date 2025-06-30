from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import numpy as np

app = Flask(__name__)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

@app.route('models/v1/embeddings', methods=['POST'])
def get_embeddings():
    data = request.json
    input_text = data.get('input', '')
    
    if isinstance(input_text, list):
        embeddings = model.encode(input_text)
    else:
        embeddings = model.encode([input_text])
        
    response = {
        "object": "list",
        "data": [
            {
                "object": "embedding",
                "embedding": embedding.tolist(),
                "index": i
            } for i, embedding in enumerate(embeddings)
        ],
        "model": "all-minilm-l6-v2",
        "usage": {
            "prompt_tokens": 0,
            "total_tokens": 0
        }
    }
    
    return jsonify(response)

@app.route('/v1/models', methods=['GET'])
def get_models():
    return jsonify({
        "object": "list",
        "data": [
            {
                "id": "all-minilm-l6-v2",
                "object": "model",
                "created": 0,
                "owned_by": "local"
            }
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5274)