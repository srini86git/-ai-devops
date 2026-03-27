from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
# Initialize the model
llm = OllamaLLM(model="qwen2.5-coder")
# Create a prompt template with variables
prompt = ChatPromptTemplate.from_template("""
Role: History Elementary Teacher
Task: {question}
Answer in a {tone} tone.
""")
# Build the chain
chain = prompt | llm
# Invoke with different variable values
response = chain.invoke({
"question": "What is the capital of India?",
"tone": "educational and simple"
})
print("Response with template:")
print(response)