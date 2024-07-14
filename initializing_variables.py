from import_libs import *
### Initializing variables
pinecone = Pinecone(api_key = PINECONE_API_KEY)


## initializing the SentenceTransformer model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = SentenceTransformer("all-MiniLM-L6-v2").to(device)

## Credentials for Pinecone
cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
region = os.environ.get('PINECONE_REGION') or 'us-east-1'
spec = ServerlessSpec(cloud=cloud, region=region)
index_name = "william"

## headers for Ollama model
headers={
    "Content-Type" : "application/json"
}

## URL for custom LLM model
URL="http://localhost:11434/api/generate"

history = []
