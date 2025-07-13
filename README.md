> **⚡ OASIS: The only AI scheduling assistant powered by real Multi-Constraint Programming (MCP) and Agent-to-Agent (A2A) collaboration. Experience the future of coordination, today.**

# OASIS  
### OMNI AGENTIC SCHEDULING INTELLIGENT SYSTEM

## 🚀 The Future of Scheduling is Here

> **💡 Stop settling for simple scheduling tools. OASIS leverages MCP and A2A to deliver solutions no other system can.**

Welcome to **OASIS**, a breakthrough solution for the [AMDAI Hackathon x E Cell IIT Mumbai](https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant) challenge.  
OASIS is the world’s first truly context aware agentic AI scheduling assistant, designed to eliminate the chaos of coordination and redefine how people, time, and projects align.

## 🏆 Why OASIS Was Created

Imagine  
Global teams scattered across continents and time zones  
High stakes deadlines, critical project updates, and the clock always ticking  
Endless email back and forth, double bookings, missed opportunities

Scheduling is no longer just a clerical task. It is a bottleneck in the age of distributed, high velocity work.

The AMDAI Hackathon, in collaboration with E Cell IIT Mumbai, set out the challenge to create an AI that goes beyond rules and routines—an assistant that reasons, adapts, and acts with true intelligence.

---

> **🚀 With OASIS’s advanced MCP and A2A, your meetings don’t just get scheduled—they get optimized across all constraints and organizations.**

## 💡 What Makes OASIS Different

### 1. Context is King

Traditional scheduling is static or rule based. OASIS is context based—it parses urgency, time zones, priorities, and even the intent behind your words.  
It knows the difference between “let’s catch up” and “this is mission critical.”

### 2. Agentic AI Beyond Automation

- Understands natural language, project context, and attendees’ roles  
- Reasons with priorities, resolves conflicts, and adapts to last minute changes  
- Acts by initiating scheduling, following up, and rescheduling autonomously

### 3. Global by Design

OASIS ensures everyone is included—no more 3AM calls for your New York team.  
It intelligently balances global calendars, work hours, and local constraints.

### 4. Seamless Integration

- Google Calendar API: Real time bi directional sync  
- vLLM and SOTA LLMs: DeepSeek 7B, Meta Llama 3.1 8B for true human class comprehension  
- Pythonic extensibility: Built for adaptability and future proofing

---

## 🚨 The Power of MCP and A2A: The OASIS Revolution

> **🔄 Tired of “find a time” emails? OASIS’s MCP engine and A2A negotiation mean you never have to think about scheduling again — even with external partners.**

### Multi-Constraint Programming (MCP): The Brain Behind OASIS

OASIS is fundamentally powered by Multi-Constraint Programming (MCP). MCP enables OASIS to simultaneously optimize across dozens of real-world variables such as time zones, role-based priorities, availability, urgency, dependencies, and stakeholder preferences.  
Unlike conventional tools that simply look for the first available slot, MCP ensures that every constraint is dynamically considered and balanced—even for the most challenging and high-stakes scheduling scenarios.

### Agent-to-Agent (A2A) Collaboration: Intelligent Negotiation

OASIS introduces Agent-to-Agent (A2A) collaboration, where scheduling agents communicate directly with each other—across teams, departments, and even between different organizations or OASIS instances.  
A2A allows OASIS to negotiate, resolve conflicts, and secure win-win time slots for all parties, breaking the barriers that hinder ordinary scheduling solutions.

With MCP and A2A working together, OASIS transforms even the most complex multi-party, multi-constraint scheduling challenge into a seamless, optimized process.

---

## 🦄 How OASIS Excels Beyond Other Solutions

While other scheduling tools:
- Only check for open slots
- Require manual intervention and negotiation
- Ignore deep context, urgency, or cross-company needs

**OASIS stands apart:**
- MCP-driven, context aware optimization: Every factor, every stakeholder, every nuance is considered
- Agentic reasoning with advanced A2A: OASIS actively negotiates with other agents across teams, companies, and even platforms
- Excels in complex scenarios: OASIS, with MCP and A2A, delivers where others fall short
- Truly global and cross-organization: OASIS finds the best time for you—even with external partners

For the hardest scheduling problems, remember two things: MCP and A2A. That is OASIS.

---

> **🌎 OASIS is not just a tool. It’s a network of intelligent agents, all working together—A2A—for you, with MCP at its core.**

## 🛠️ The OASIS Solution In Action

### How OASIS Works

1. Parses Email Request: Uses LLM to extract attendees, urgency, duration, and constraints from natural language
2. Scans Calendars: Pulls real time events for all participants via Google Calendar API
3. Contextual Reasoning: Assesses urgency, time zones, and priorities. Suggests optimal times, not just available times
4. Schedules Autonomously: Books the meeting, updates all calendars, and notifies attendees
5. Learns Preferences: Remembers recurring patterns and personalizes future scheduling

## 🏅 Types of Scheduling

- Static: Fixed slots, low flexibility  
- Rule Based: Simple logic, quickly breaks in complex scenarios  
- Dynamic: Reacts to changes, lacks deep understanding  
- Priority Based: Considers importance, ignores full context  
- Context Based (OASIS): Understands intent, urgency, time zones, and real world constraints—this is the new gold standard

## 🦾 What We’re Doing Differently

No more micromanagement: OASIS acts as your tireless scheduling chief of staff  
No more one size fits all: Each meeting is unique, with context and stakeholder needs at the forefront  
No more basic automation: This is agentic intelligence, not robotic repetition

---

## 🔮 Future Scope: The OASIS Vision

- Personalized Scheduling Agents: OASIS will adapt uniquely to you and your team  
- Cross Platform Integration: Beyond Google—Microsoft, Apple, Slack, Teams  
- Recurrence & Smart Suggestions: Handles recurring meetings with adaptive, context aware logic  
- Federated Privacy: Schedules collaboratively without exposing private data  
- Voice & Multimodal Interfaces: Speak, type, or tap—OASIS will understand  
- Multi Agent Negotiation: OASIS agents can negotiate between organizations, projects, and external partners for seamless coordination

---

> **🧠 When you need real intelligence, real negotiation, and real optimization—MCP and A2A inside OASIS deliver. Don’t just schedule. Orchestrate.**

## 📝 How to Use OASIS

1. **Clone the repo**
    ```bash
    git clone https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant.git
    cd AI-Scheduling-Assistant
    ```
2. **Set up dependencies**  
   Ensure Python environment and install required packages from `requirements.txt`

3. **Launch vLLM server**  
   For [DeepSeek LLM 7B](https://github.com/deepseek-ai/DeepSeek-LLM) or [Meta Llama 3.1 8B](https://ai.meta.com/resources/models-and-libraries/llama-downloads/) run
    ```bash
    HIP_VISIBLE_DEVICES=0 vllm serve /home/user/Models/deepseek-ai/deepseek-llm-7b-chat --gpu-memory-utilization 0.9 --swap-space 16 --host 0.0.0.0 --port 3000
    ```

4. **Configure Google Calendar API**  
   Place your credentials as per the instructions in `Calendar_Event_Extraction` notebook

5. **Run the assistant**  
   Call the main function in your Python code
    ```python
    from solution import your_meeting_assistant
    result = your_meeting_assistant(input_json)
    print(result)
    ```

## 🗂️ Input Output Format

### Input Format

```json
{
    "Request_id": "comprehensive-test-001",
    "Datetime": "02-07-2025T12:34:55",
    "Location": "IIT Mumbai",
    "From": "teamadmin.amd@gmail.com",
    "Attendees": [
        {"email": "userone.amd@gmail.com"},
        {"email": "usertwo.amd@gmail.com"},
        {"email": "userthree.amd@gmail.com"}
    ],
    "Subject": "Comprehensive AI Scheduling Test - Multi-Agent Coordination",
    "EmailContent": "Hi Team! This is an urgent meeting request. We need to discuss the Agentic AI Project status update. Please schedule a 45-minute meeting for next Monday at 3:00 PM IST. This is critical for our project timeline. Also, we need to coordinate with the New York team, so please ensure the time works for everyone across timezones. The meeting should cover: 1) Project milestones, 2) Resource allocation, 3) Risk assessment, and 4) Next steps. Please make sure all stakeholders can attend."
}
```

### Output Format

```json
{
    "Request_id": "comprehensive-test-001",
    "Datetime": "02-07-2025T12:34:55",
    "Location": "IIT Mumbai",
    "From": "teamadmin.amd@gmail.com",
    "Attendees": [
        {
            "email": "userone.amd@gmail.com",
            "events": [
                {
                    "StartTime": "2025-07-14T15:00:00+05:30",
                    "EndTime": "2025-07-14T15:45:00+05:30",
                    "NumAttendees": 4,
                    "Attendees": [
                        "teamadmin.amd@gmail.com",
                        "userone.amd@gmail.com",
                        "usertwo.amd@gmail.com",
                        "userthree.amd@gmail.com"
                    ],
                    "Summary": "Comprehensive AI Scheduling Test - Multi-Agent Coordination"
                }
            ]
        },
        {
            "email": "usertwo.amd@gmail.com",
            "events": [
                {
                    "StartTime": "2025-07-14T15:00:00+05:30",
                    "EndTime": "2025-07-14T15:45:00+05:30",
                    "NumAttendees": 4,
                    "Attendees": [
                        "teamadmin.amd@gmail.com",
                        "userone.amd@gmail.com",
                        "usertwo.amd@gmail.com",
                        "userthree.amd@gmail.com"
                    ],
                    "Summary": "Comprehensive AI Scheduling Test - Multi-Agent Coordination"
                }
            ]
        },
        {
            "email": "userthree.amd@gmail.com",
            "events": [
                {
                    "StartTime": "2025-07-14T15:00:00+05:30",
                    "EndTime": "2025-07-14T15:45:00+05:30",
                    "NumAttendees": 4,
                    "Attendees": [
                        "teamadmin.amd@gmail.com",
                        "userone.amd@gmail.com",
                        "usertwo.amd@gmail.com",
                        "userthree.amd@gmail.com"
                    ],
                    "Summary": "Comprehensive AI Scheduling Test - Multi-Agent Coordination"
                }
            ]
        }
    ],
    "Subject": "Comprehensive AI Scheduling Test - Multi-Agent Coordination",
    "EmailContent": "Hi Team! This is an urgent meeting request. We need to discuss the Agentic AI Project status update. Please schedule a 45-minute meeting for next Monday at 3:00 PM IST. This is critical for our project timeline. Also, we need to coordinate with the New York team, so please ensure the time works for everyone across timezones. The meeting should cover: 1) Project milestones, 2) Resource allocation, 3) Risk assessment, and 4) Next steps. Please make sure all stakeholders can attend.",
    "EventStart": "2025-07-14T15:00:00+05:30",
    "EventEnd": "2025-07-14T15:45:00+05:30",
    "Duration_mins": "45",
    "MetaData": {}
}
```

---

> **🎯 OASIS, with MCP and A2A, is your competitive edge in the modern, interconnected workplace. Welcome to a new era of intelligent scheduling.**

## 💬 Acknowledgements

Grateful for the inspiration and support from **AMDAI Hackathon Team** and **E Cell IIT Mumbai**  
Thank you for pushing us to build the future together

## 🤝 Join the Revolution

OASIS is open for collaboration, feedback, and contributions.  
Raise an issue, star the repo, and help us build the next era of agentic AI.

> **OASIS isn’t just a scheduling tool. It is the dawn of intelligent, context-driven collaboration, powered by MCP and A2A. Welcome to the future.**
