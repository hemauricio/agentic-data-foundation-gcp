import os
from langchain_google_vertexai import ChatVertexAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent


project_id = os.getenv("PROJECT_ID")
dataset_id = os.getenv("BIGQUERY_DATASET")

# 1. Initialize Gemini 1.5 Pro via Vertex AI
print("Initializing Agent...")
# llm = ChatVertexAI(model_name="gemini-1.5-pro-001", temperature=0)
llm = ChatVertexAI(
    model_name="gemini-1.5-pro", 
    project=project_id, 
    location="us-central1", 
    temperature=0
)

# 2. Connect to your BigQuery Dataset

# SQLAlchemy uses this specific format for BigQuery connections
sqlalchemy_url = f"bigquery://{project_id}/{dataset_id}"
db = SQLDatabase.from_uri(sqlalchemy_url)

# 3. Create the LangChain Agent
# We set verbose=True so you can watch Gemini "think" in your terminal
agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="tool-calling",
    verbose=True 
)

# 4. Give the Agent a natural language task
question = "What is the average tenure of customers who churned versus customers who did not churn?"
print(f"\nQuestion: {question}\n")

# 5. Execute!
response = agent_executor.invoke({"input": question})

print("\n==================================")
print(f"Final Answer: {response['output']}")
print("==================================")
