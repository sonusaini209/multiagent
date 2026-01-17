# 🛍️ OmniLife: Hierarchical Multi-Agent System

OmniLife is a state-of-the-art **Hierarchical Multi-Agent Orchestrator** designed to break down data silos. This system unifies four independent retail databases—**ShopCore**, **ShipStream**, **PayGuard**, and **CareDesk**—allowing a single "Super Agent" to resolve complex customer queries that span multiple departments.

## 🔗 Live Deployment
**Demo Link:** https://multiagent-zplg.onrender.com/

---

##  System Architecture

The project is built using **LangGraph** to create a stateful, circular workflow between a supervisor and specialized workers.

* **Super Agent (Orchestrator):** Acts as the brain. It analyzes natural language, determines which departments are needed, and synthesizes raw data into a human-friendly response.
* **Sub-Agents (Text-to-SQL):** Four specialized agents that generate and execute SQL queries against their own isolated SQLite databases.
* **Contextual Memory:** The system maintains a shared state, allowing an `OrderID` or `UserID` found by one agent to be passed as a dependency to the next.



---

##  The Data Ecosystem

The system automatically initializes four isolated relational databases with synthetic data, ensuring cross-referenced IDs (like **UserID: 1** and **Order: 5001**) to test multi-hop reasoning.

| Database | Domain | Key Tables |
| :--- | :--- | :--- |
| **ShopCore** | E-commerce | Users, Products, Orders |
| **ShipStream** | Logistics | Shipments, Warehouses, Tracking Events |
| **PayGuard** | Finance | Wallets, Transactions, Payment Methods |
| **CareDesk** | Support | Tickets, Messages, Satisfaction Surveys |

---

## Demonstration: The "Thought Process" Log

Below is a trace of the Super Agent coordinating sub-agents for a high-complexity query.

### **Query:** *"Where is my Gaming Monitor and what is my ticket status?"*

1.  **Orchestrator Analysis:** Identifying keywords "Gaming Monitor" (ShopCore) and "ticket status" (CareDesk). Realizes it needs an `OrderID` to get tracking (ShipStream).
2.  **Step 1: ShopCore Agent:** Finds that the "Gaming Monitor" belongs to `Order #5001`.
    * *Result:* `{"product": "Gaming Monitor", "order_id": 5001, "user_id": 1}`
3.  **Step 2: ShipStream Agent:** Uses `Order #5001` to fetch logistics data.
    * *Result:* `{"tracking_no": "TRK12345", "status": "In Transit", "ETA": "2026-01-20"}`
4.  **Step 3: CareDesk Agent:** Uses `User #1` to check for open tickets.
    * *Result:* `{"ticket_id": 801, "issue": "Delivery Delay", "status": "Assigned"}`
5.  **Final Synthesis:** "Your Gaming Monitor (Order #5001) is currently in transit with tracking number TRK12345, expected by Jan 20th. Your support ticket (#801) is already assigned to an agent for review."



---

## 💻 Local Setup & Installation

1.  **Clone the Repo:**
    ```bash
    git clone [https://github.com/your-username/omnilife-ai.git](https://github.com/your-username/omnilife-ai.git)
    cd omnilife-ai
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Environment Variables:**
    Create a `.env` file and add: `OPENAI_API_KEY=your_key_here`
4.  **Launch the UI:**
    ```bash
    streamlit run app.py
    ```
