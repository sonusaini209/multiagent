# OmniLife: Hierarchical Multi-Agent System

[cite_start]A system built with LangGraph and OpenAI to unify four siloed product databases (ShopCore, ShipStream, PayGuard, CareDesk)[cite: 1, 4, 6].

## ⚙️ How it Works
1. [cite_start]**Orchestrator**: Parses natural language and decides the sequence of execution[cite: 1, 9].
2. [cite_start]**Sub-Agents**: Generate SQL queries against isolated SQLite databases and return structured JSON[cite: 1, 10, 55].
3. [cite_start]**Dependencies**: The system passes OrderIDs and UserIDs between agents to resolve multi-domain queries[cite: 1, 51].

## 📊 Demo Scenarios
### Scenario: The Complex Query
**Query**: "Where is my Gaming Monitor and what is my ticket status?"
- [cite_start]**Step 1 (ShopCore)**: Found OrderID `5001` for User `1`[cite: 1, 62].
- [cite_start]**Step 2 (ShipStream)**: Used `5001` to find tracking number `TRK12345`[cite: 1, 63].
- [cite_start]**Step 3 (CareDesk)**: Found Ticket `801` is "Assigned"[cite: 1, 64].
- [cite_start]**Synthesized Result**: "Your Gaming Monitor (Order 5001) is in transit (TRK12345) and your support ticket is currently assigned." [cite: 1, 65]

## 🛠️ Installation
1. Install requirements: `pip install -r requirements.txt`
2. Add `OPENAI_API_KEY` to a `.env` file.
3. Run the UI: `streamlit run app.py`
