# GraphRAG with Foundry Local

This repository contains a setup for running GraphRAG (Retrieval-Augmented Generation with Graph) using locally deployed models via Foundry Local.

## Setup Instructions

### 1. Install GraphRAG

First, set up a Python virtual environment and install GraphRAG:

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install GraphRAG
pip install graphrag

# Clone this repo if you haven't already
git clone https://github.com/doruit/Graphrag-Foundry-Local.git
cd Graphrag-Foundry-Local
```

For more detailed instructions, follow the [official GraphRAG documentation](https://microsoft.github.io/graphrag/get_started/).

### 2. Install Foundry Local

Install Foundry Local to run LLMs on your machine:

```bash
# Install Foundry Local CLI
pip install "foundry-local[cli]"

# Verify installation
foundry --version
```

For detailed installation instructions, see the [Foundry Local documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-local/get-started).

### 3. Run Mistral-7B Model Locally

Start the Mistral-7B model using Foundry Local:

```bash
foundry model run mistral-7b-v0.2
```

The model will start downloading (if not already present) and then run. **Note the port number in the output** (typically 5273).

### 4. Test the Model

Verify the model is running correctly:

```bash
# Check available models
curl http://localhost:5273/v1/models

# Test with a simple query
curl http://localhost:5273/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-7b-v0.2",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

### 5. Install and Run Embedding Model Locally

We'll use the all-minilm-l6-v2 model for embeddings:

```bash
# Create a directory for the model
mkdir -p ./models/all-minilm-l6-v2 && cd ./models/all-minilm-l6-v2

# Clone the model from Hugging Face
git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 .

# Install sentence-transformers
pip install sentence-transformers flask

# Copy the server script to the models/all-minilm-l6-v2 folder 
cp /embeddings_server.py /models/all-minilm-l6-v2/  

# Start the embedding server
python server.py
```

The embedding server will run on port 5274. Ensure that the `server.py` file is available in the `models/all-minilm-l6-v2` directory.

### 6. Update Configuration

Edit the `ragtest/settings.yaml` file to reflect the correct port numbers for both models:

```yaml
models:
  default_chat_model:
    type: openai_chat
    api_base: http://localhost:5273/v1  # Update with your LLM port
    api_key: not-needed
    model: mistral-7b-v0.2
    encoding_model: cl100k_base
    model_supports_json: true
    # ...other settings...
  
  default_embedding_model:
    type: openai_embedding
    api_base: http://localhost:5274/v1  # Update with your embedding server port
    api_key: not-needed
    model: all-minilm-l6-v2
    encoding_model: cl100k_base
    dimensions: 384
    # ...other settings...
```

### 7. Run the GraphRAG Indexing Pipeline

In a new terminal window (with the virtual environment activated):

```bash
graphrag index --root ./ragtest
```

This will start the indexing process using your locally running models.

## Troubleshooting

- If you encounter port conflicts, you can modify the ports in both the server scripts and the `settings.yaml` file.
- Ensure both model servers are running before starting the GraphRAG indexing process.
- Check the log files in the `ragtest/logs` directory for detailed error information.

## Additional Resources

- [GraphRAG Documentation](https://microsoft.github.io/graphrag/)
- [Foundry Local Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-local/)
- [Sentence Transformers](https://www.sbert.net/)