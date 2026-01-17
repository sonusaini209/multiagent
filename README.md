# OmniLife: Hierarchical Multi-Agent Orchestrator

[cite_start]This repository contains a **Hierarchical Multi-Agent System** designed to unify the customer support experience for "OmniLife," a conglomerate with four siloed product databases[cite: 4, 6].

## 🚀 Live Demo
**Render/Streamlit App:** [INSERT_YOUR_DEPLOYED_URL_HERE]

## 🛠️ System Architecture
[cite_start]The system consists of a **Super Agent (Orchestrator)** and four specialized **Sub-Agents**[cite: 8]:
- [cite_start]**ShopCore Agent**: Manages user accounts and orders[cite: 14].
- [cite_start]**ShipStream Agent**: Handles logistics and tracking via OrderID[cite: 21, 28].
- [cite_start]**PayGuard Agent**: Manages transactions and refunds[cite: 29].
- [cite_start]**CareDesk Agent**: Tracks support tickets and disputes[cite: 39].

### The "Thought Process"
The Orchestrator uses **LangGraph** to maintain a state machine. [cite_start]It parses natural language, identifies dependencies (e.g., fetching an OrderID before checking a tracking status), and synthesizes a final answer from structured JSON data[cite: 48, 51, 55].



## 📊 Database Schema
The system automatically generates four SQLite databases with synthetic data, ensuring that:
- [cite_start]**UserID 1** and **OrderID 5001** are linked across all platforms to facilitate complex "Gaming Monitor" queries[cite: 60, 68].

## 💻 Installation & Local Setup

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/yourusername/omnilife-multiagent.git](https://github.com/yourusername/omnilife-multiagent.git)
   cd omnilife-multiagent
