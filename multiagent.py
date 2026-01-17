import os
import json
from typing import TypedDict, List, Dict, Any
from sqlalchemy import create_engine
#from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint

# Replace your old OpenAI initialization with this:
model = HuggingFaceEndpoint(
    repo_id="meta-llama/Meta-Llama-3-8B-Instruct", # A very capable free model
    task="text-generation",
    huggingfacehub_api_token="your_huggingface_api_token_here",
    temperature=0.1
)
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

# 1. Define the State
class AgentState(TypedDict):
    user_query: str
    selected_agents: List[str]
    responses: Dict[str, str]
    final_answer: str

# 2. Initialize the Model
#model = ChatOpenAI(temperature=0, model_name="gpt-4")
model = HuggingFaceEndpoint(
    repo_id="meta-llama/Meta-Llama-3-8B-Instruct", # A very capable free model
    task="text-generation",
    huggingfacehub_api_token="your_huggingface_api_token_here",
    temperature=0.1
)

import sqlite3

# Define the precise requirements for each database
db_specs = {
    "DB_ShopCore.db": {
        "features": "User accounts, product catalog, and initial order placement.",
        "tables": "Users (UserID, Name, Email, PremiumStatus), Products (ProductID, Name, Category, Price), Orders (OrderID, UserID, ProductID, OrderDate, Status)"
    },
    "DB_ShipStream.db": {
        "features": "Logistics, movement of goods, and warehouses.",
        "tables": "Shipments (ShipmentID, OrderID, TrackingNumber, EstimatedArrival), Warehouses (WarehouseID, Location, ManagerName), TrackingEvents (EventID, ShipmentID, WarehouseID, Timestamp, StatusUpdate)"
    },
    "DB_PayGuard.db": {
        "features": "Wallet management, payment processing, and refunds.",
        "tables": "Wallets (WalletID, UserID, Balance, Currency), Transactions (TransactionID, WalletID, OrderID, Amount, Type), PaymentMethods (MethodID, WalletID, Provider, ExpiryDate)"
    },
    "DB_CareDesk.db": {
        "features": "Tickets, disputes, and customer satisfaction.",
        "tables": "Tickets (TicketID, UserID, ReferenceID, IssueType, Status), TicketMessages (MessageID, TicketID, Sender, Content), SatisfactionSurveys (SurveyID, TicketID, Rating, Comments)"
    }
}

for db_name, spec in db_specs.items():
    # Force the LLM to generate the FULL SQL (Create + Insert) in one go
    prompt = f"""
    Generate ONLY raw SQLite SQL for the database {db_name}.
    Context: {spec['features']}
    Mandatory Tables: {spec['tables']}
    
    Requirements:
    1. Start with DROP TABLE IF EXISTS for all mentioned tables.
    2. CREATE all 3 tables with appropriate data types.
    3. INSERT exactly 5 rows of synthetic data per table.
    4. CRITICAL: In all databases, ensure references to UserID 1 and OrderID 5001 (linked to a 'Gaming Monitor').
    
    Return ONLY the raw SQL code. No words, no markdown blocks.
    """
    
    sql_script = model.invoke(prompt).content.replace("```sql", "").replace("```", "").strip()
    
    with sqlite3.connect(db_name) as conn:
        try:
            conn.executescript(sql_script)
            print(f"Successfully created and populated: {db_name}")
        except Exception as e:
            print(f" Error in {db_name}: {e}")

# Verification Step: List tables in each DB
print("\n--- FINAL SCHEMA VERIFICATION ---")
for db in db_specs.keys():
    with sqlite3.connect(db) as conn:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall() if not row[0].startswith('sqlite_')]
        print(f"{db}: {tables}")


# 3. Define Sub-Agent Logic
def create_db_agent(db_path: str, query: str):
    """Helper to execute SQL queries for sub-agents."""
    try:
        engine = create_engine(f'sqlite:///{db_path}')
        db = SQLDatabase(engine)
        # Using from_llm as SQLDatabaseChain with llm is deprecated
        db_chain = SQLDatabaseChain.from_llm(llm=model, db=db, verbose=False)
        return db_chain.run(query)
    except Exception as e:
        return f"Error accessing {db_path}: {str(e)}"

def shopcore_agent(state: AgentState):
    res = create_db_agent('DB_ShopCore.db', state['user_query'])
    return {"responses": {**state.get('responses', {}), "ShopCore": res}}

def shipstream_agent(state: AgentState):
    res = create_db_agent('DB_ShipStream.db', state['user_query'])
    return {"responses": {**state.get('responses', {}), "ShipStream": res}}

def caredesk_agent(state: AgentState):
    res = create_db_agent('DB_CareDesk.db', state['user_query'])
    return {"responses": {**state.get('responses', {}), "CareDesk": res}}

def PayGuard_agent(state: AgentState):
    res = create_db_agent('DB_PayGuard.db', state['user_query'])
    return {"responses": {**state.get('responses', {}), "PayGuard": res}}

# 4. Define Supervisor/Orchestrator
def supervisor(state: AgentState):
    prompt = f"""You are a supervisor agent for Omni-Retail.
    Decompose the user query and select which agents are required:
    - ShopCoreAgent (Orders/Products)
    - ShipStreamAgent (Tracking/Logistics)
    - CareDeskAgent (Tickets/Support)
    - PayGuardAgent (Payments)
    
    Return ONLY a JSON list of strings (e.g., ["ShopCoreAgent", "ShipStreamAgent"]).
    User Query: {state['user_query']}"""
    
    response = model.invoke(prompt).content
    try:
        selected = json.loads(response)
    except:
        selected = ["ShopCoreAgent"] # Fallback
    
    return {"selected_agents": selected}

def synthesizer(state: AgentState):
    """Final node to combine all sub-agent data into one response."""
    context = json.dumps(state['responses'])
    prompt = f"Based on the following data from different departments: {context}\n\nProvide a final answer to the user: {state['user_query']}"
    res = model.invoke(prompt).content
    return {"final_answer": res}

# 5. Routing Logic
def router(state: AgentState):
    # Logic to decide which node to visit next based on selected_agents
    if not state.get('selected_agents'):
        return "synthesizer"
    
    next_agent = state['selected_agents'].pop(0)
    mapping = {
        "ShopCoreAgent": "shopcore",
        "ShipStreamAgent": "shipstream",
        "CareDeskAgent": "caredesk",
        "PayGuardAgent": "PayGuard"
    }
    return mapping.get(next_agent, "synthesizer")

# 6. Build the Graph
builder = StateGraph(AgentState)

builder.add_node("supervisor", supervisor)
builder.add_node("shopcore", shopcore_agent)
builder.add_node("shipstream", shipstream_agent)
builder.add_node("caredesk", caredesk_agent)
builder.add_node("PayGuard", PayGuard_agent)
builder.add_node("synthesizer", synthesizer)

builder.add_edge(START, "supervisor")

# Conditional routing from supervisor and after each agent back to the router
builder.add_conditional_edges("supervisor", router)
builder.add_conditional_edges("shopcore", router)
builder.add_conditional_edges("shipstream", router)
builder.add_conditional_edges("caredesk", router)
builder.add_conditional_edges("PayGuard", router)

builder.add_edge("synthesizer", END)

workflow = builder.compile()

# Example Execution
result = workflow.invoke({"user_query": "I ordered a Gaming Monitor, where is it?"})

print(result['final_answer'])
