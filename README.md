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
