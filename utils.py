# This Module contains the helper functions for the  tutor.ai

from initializing_variables import *

##Methods
##1. connect to vector database(pdf_to_pinecone())
##2. Retrive the the semantic Results from the vector database function (Retrive())
##3. Generate the response from the prompt using the custom LLM model generate()


def pdf_to_pinecone(pdf_path, host, index_name):

    pinecone = Pinecone(api_key = PINECONE_API_KEY)

    if index_name not in pinecone.list_indexes().names():
        pinecone.create_index(index_name, dimension=384, spec = spec)  # Adjust dimension based on your model
    
    # Connect to the index
    index = pinecone.Index(index_name)
    
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        # Extract text from each page
        text = ""
        for page in reader.pages:
            text += page.extract_text() + " "
        
        # Split the text into chunks (adjust chunk_size as needed)
        chunk_size = 1000
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
        # Convert chunks to vectors and store in Pinecone
        for i, chunk in enumerate(chunks):
            # Generate vector embedding
            vector = model.encode(chunk).tolist()
            
            # Create a unique ID for each vector
            vector_id = f"{os.path.basename(pdf_path)}_{i}"
            
            # Upsert the vector into Pinecone
            index.upsert(vectors=[(vector_id, vector, {"text": chunk})])
    
    print(f"PDF '{pdf_path}' has been processed and stored in Pinecone index '{index_name}'")
    return index


def retrieve(query, index):
    # res = openai.Embedding.create(
    #     input=[query],
    #     engine=embed_model
    # )
    res = model.encode(query).tolist()
    print("result", res)

    # retrieve from Pinecone
    xq = res

    # get relevant contexts
    contexts = []
    time_waited = 0
    while (len(contexts) < 3 and time_waited < 60 * 12):
        res = index.query(vector=xq, top_k=3, include_metadata=True)
        contexts = contexts + [
            x['metadata']['text'] for x in res['matches']
        ]
        print(f"Retrieved {len(contexts)} contexts, sleeping for 15 seconds...")
        time.sleep(5)
        time_waited += 15

    if time_waited >= 60 * 12:
        print("Timed out waiting for contexts to be retrieved.")
        contexts = ["No contexts retrieved. Try to answer the question yourself!"]


    # build our prompt with the retrieved contexts included
    prompt_start = (
        "Answer the question based on the context below.\n\n"+
        "Context:\n"
    )
    prompt_end = (
        f"\n\nQuestion: {query}\nAnswer:"
    )
    # append contexts until hitting limit
    for i in range(1, len(contexts)):
        if len("\n\n---\n\n".join(contexts[:i])) >= LIMIT:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(contexts[:i-1]) +
                prompt_end
            )
            break
        elif i == len(contexts)-1:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(contexts) +
                prompt_end
            )
    print(prompt)
    return prompt

def generate_response(prompt):
    history.append(prompt)
    final_prompt="\n".join(history)
    data={
        "model" : MODEL_NAME,
        "prompt" : final_prompt,
        "stream" : False
    }

    response = requests.post(URL, headers=headers, data=json.dumps(data))


    if response.status_code==200:
        response= response.text
        data = json.loads(response)
        actual_response=data["response"]
        return actual_response
    else:
        print("error: status_code:= ",response.status_code)

pdf_path = "william_shakespeare.pdf"
host = "https://dl-ai11-oqaxo3q.svc.aped-4627-b74a.pinecone.io"
index_name = "william"

prompt = "tell me some of the best works of william shakespeare"

index = pdf_to_pinecone(pdf_path, host, index_name)

print("data is stored from pdf to Pinecone database!!!")

final_prompt = retrieve(prompt, index)
print("prompt is recieved from the database now generating the response")

actual_response = generate_response(final_prompt)

print(actual_response)
