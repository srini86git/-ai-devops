from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
# Initialize the model
llm = OllamaLLM(model="qwen3:1.7b")
# Create a reusable prompt template
prompt = ChatPromptTemplate.from_template("""
Role: {role}
Task: {question}
Answer in a {tone} tone.
""")
# Build the chain once
chain = prompt | llm
# Use the same template for multiple different queries
queries = [
{
"role": "History Elementary Teacher",
"question": "What is the capital of America?",
"tone": "educational and simple"
},
{
"role": "Science Teacher",
"question": "Why is the sea blue?",
"tone": "fun and engaging"
},
{
"role": "Travel Guide",
"question": "What are the top 3 places to visit in chennai?",
"tone": "exciting and descriptive"
}
]
# Loop through each query and get responses
for i, query in enumerate(queries, 1):
    print(f"\nquery {i}:")
    print(f"Role: {query['role']}")
    print(f"Question: {query['question']}")
    print(f"Tone: {query['tone']}")
    print("-" * 40)
    response = chain.invoke(query)
    print(f"Response: {response}\n")