# 🤖 AI Scheduling Assistant with MCP & A2A Architecture

[![Built with Python](https://img.shields.io/badge/Built%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![LLM-Powered](https://img.shields.io/badge/Powered%20by-LLM-blueviolet?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![Google Calendar API](https://img.shields.io/badge/Google%20Calendar%20API-Enabled-34A853?style=for-the-badge&logo=google-calendar&logoColor=white)](https://developers.google.com/calendar)
[![MCP Architecture](https://img.shields.io/badge/Architecture-MCP%20%26%20A2A-orange?style=for-the-badge)]()
[![Flask API](https://img.shields.io/badge/API-Flask%20REST%20Server-lightgrey?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)

---

> ⚡ **The next-gen scheduling assistant: Modular, intelligent, and autonomous — built on MCP and A2A for truly effortless meetings.**  

---

## 🧠 Project Overview

**AI Scheduling Assistant** is a smart, agent-powered system that automates meeting scheduling using:
- ✅ Live Google Calendar integration
- ✅ Modular Agent Architecture (MCP Protocol)
- ✅ Agent-to-Agent negotiation (A2A)
- ✅ LLMs to parse human-written meeting emails
- ✅ Direct timezone verification for globally distributed teams

> 🌟 **MCP (Multi-Constraint Programming) and A2A (Agent-to-Agent) negotiation ensure every meeting respects all your constraints, priorities, and people — not just the first open slot.**

Built to be modular, intelligent, and fully autonomous — perfect for remote teams, corporate calendars, and personal AI agents.

---

## 🧩 Architecture Highlights

### 🔷 MCP: Modular Command Protocol

> **Every core task is handled by a dedicated agent module. Agents operate independently and communicate via robust internal interfaces.** MCP enables optimal scheduling even in complex, multi-constraint scenarios.

| Module               | Responsibility                             |
|----------------------|--------------------------------------------|
| `BossAgent`          | Orchestrates scheduling & final decision   |
| `EmployeeAgent`      | Accesses calendar, finds slots, negotiates |
| `MeetingParserAgent` | Parses human-like meeting emails           |
| `TimezoneAgent`      | Validates global timezone compatibility    |

✅ **Loosely coupled. Easily extendable. Fully testable.**

---

### 🔁 A2A: Agent-to-Agent Negotiation

> **A2A is what sets us apart.** Agents discuss among themselves to finalize the best meeting time:
- Each `EmployeeAgent` proposes available slots.
- They analyze others’ proposals and negotiate using LLMs.
- Final time is picked with maximum consensus by the `BossAgent`.

---

## 🔥 Key Features

### ✅ Real-Time Google Calendar Integration
- Authenticated access for each employee's calendar
- Reads live events using Google API
- Adds new scheduled meetings automatically

### 🧠 LLM-Based Understanding
- Parses natural language meeting requests like:  
  _"Let's do 45 mins next Thursday around 3 PM. It's urgent."_
- Extracts:
  - Duration
  - Urgency
  - Preferred time

### 🧠 AI Slot Discovery
- Uses LLM to suggest optimal 30–60 min time slots
- Honors business hours: 9AM–6PM
- Provides confidence scores for each slot

### 🌐 Timezone Compatibility Agent
- Checks if each employee is **within working hours**
- Provides alternate suggestion (e.g., 4PM IST → 6:30AM EST)

### 🔁 AI Agent Negotiation (A2A)
- Each agent compares its slots with others
- Uses LLM to agree on the **most compatible time**

### 🔐 Fallback-First Architecture
- Every AI call has a graceful fallback mechanism
- Ensures reliability even if AI or network fails

### 📡 Flask API Server
- Endpoint: `POST /receive`
- Input: JSON-based meeting request
- Output: Fully formatted meeting metadata with calendar state

---

> 💬 **With MCP and A2A, this assistant doesn’t just automate — it collaborates, negotiates, and optimizes for you.**

---

## 📦 Sample Input

```json
{
  "Request_id": "123456",
  "Datetime": "13-07-2025T10:00:00",
  "Location": "Zoom",
  "From": "userone.amd@gmail.com",
  "Attendees": [
    {"email": "usertwo.amd@gmail.com"},
    {"email": "userthree.amd@gmail.com"}
  ],
  "Subject": "Project Sync",
  "EmailContent": "Hey team, can we do a 45-minute sync this Thursday afternoon? It’s urgent."
}
```

---

## 🖥️ Sample Output (AI Scheduled)

```json
{
  "EventStart": "2025-07-17T16:00:00+05:30",
  "EventEnd": "2025-07-17T16:45:00+05:30",
  "Attendees": [
    {
      "email": "usertwo.amd@gmail.com",
      "events": [...]
    }
  ],
  "MetaData": {
    "timezone_verification": {...},
    "scheduling_step": "Boss Agent verified timezone compatibility before scheduling"
  }
}
```

---

## 🛠️ Tech Stack

| Component       | Technology               |
|----------------|--------------------------|
| Backend Server | Flask                    |
| AI Model       | DeepSeek/LLM (7B)        |
| Auth           | Google OAuth2            |
| Calendar       | Google Calendar API v3   |
| Timezones      | `pytz`, `datetime`       |
| AI Fallbacks   | Hard-coded slot logic    |

---

## 🧪 Run Locally

1. **Clone the repo**
2. **Install requirements**  
   ```bash
   pip install -r requirements.txt
   ```
3. **Start your LLM server locally** (e.g., OpenRouter or DeepSeek)
4. **Run Flask**
   ```bash
   python app.py
   ```

---

## 🤝 Contribution Ideas

- Add meeting cancellation/rescheduling flow
- Support Microsoft Outlook calendars
- Train a fine-tuned model for better negotiation
- Add web UI dashboard (Next.js frontend)

---

## 📜 License

MIT License. Free to use, extend, and adapt for any scheduling platform or AI assistant framework.

---

> ✨ **MCP and A2A make this assistant more than just a bot — it’s your personal, always-on, negotiation-ready scheduling team.**

---

### 🚀 Let the agents handle your calendar. You focus on what matters.
