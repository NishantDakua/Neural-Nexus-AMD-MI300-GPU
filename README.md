# OASIS  
### OMNI AGENTIC SCHEDULING INTELLIGENT SYSTEM

## 🚀 The Future of Scheduling is Here

Welcome to **OASIS**—our breakthrough solution to the [AMDAI Hackathon x E Cell IIT Mumbai](https://github.com/AMD-AI-HACKATHON/AI-Scheduling-Assistant) challenge.  
This is not just a scheduling tool. OASIS is a **context aware agentic AI scheduling assistant** designed to destroy the chaos of coordination and redefine how people time and projects align.

## 🏆 Why OASIS Was Born

Imagine  
Global teams scattered across continents and time zones  
High stakes deadlines critical project updates and the clock always ticking  
Endless email back and forth double bookings missed opportunities

**Scheduling isn’t a clerical task anymore. It’s a bottleneck in the age of distributed high velocity work.**

The AMDAI Hackathon in collaboration with E Cell IIT Mumbai challenged us to create an AI that goes beyond rules and routines an assistant that reasons adapts and acts with true intelligence.

## 💡 What Makes OASIS Different

### 🌐 1 Context is King

Traditional scheduling is static or rule based. OASIS is **context based** it parses urgency timezones priorities and even the intent behind your words.  
It knows the difference between “Let’s catch up” and “This is mission critical.”

### 🧠 2 Agentic AI More Than Automation

**Understands** Natural language project context attendees’ roles  
**Reasons** Prioritizes resolves conflicts adapts to last minute changes  
**Acts** Initiates scheduling follows up reschedules autonomously

### 🌍 3 Global by Design

OASIS ensures *everyone* is included no more 3AM calls for your New York team  
It intelligently balances global calendars work hours and local constraints

### 🔗 4 Seamless Integration

**Google Calendar API** Real time bi directional sync  
**vLLM + SOTA LLMs** DeepSeek 7B Meta Llama 3.1 8B for human class comprehension  
**Pythonic Extensibility** Built for easy adaptation and future proofing

## 🛠️ The OASIS Solution In Action

### How OASIS Works

1. **Parses Email Request** Uses LLM to extract attendees urgency duration and constraints from natural language
2. **Scans Calendars** Pulls real time events for all participants via Google Calendar API
3. **Contextual Reasoning** Assesses urgency time zones and priorities Suggests optimal times not just available times
4. **Schedules Autonomously** Books the meeting updates all calendars and notifies attendees
5. **Learns Preferences** Remembers recurring patterns and personalizes future scheduling

## 🏅 What Types of Scheduling Exist

**Static** Fixed slots low flexibility  
**Rule Based** If then logic quickly breaks in complex scenarios  
**Dynamic** Reacts to changes but lacks deep understanding  
**Priority Based** Considers importance but ignores context  
**👑 Context Based OASIS** Understands intent urgency time zones and real world constraints the new gold standard

## 🦾 What We’re Doing Differently

No more human micromanagement OASIS acts as your tireless scheduling chief of staff  
No more one size fits all Each meeting is treated as unique with context and stakeholder needs always at the forefront  
No more just automation This is *agentic intelligence* not robotic repetition

## 🔮 Future Scope The OASIS Vision

**Personalized Scheduling Agents** OASIS will adapt uniquely to you and your team  
**Cross Platform Integration** Beyond Google Microsoft Apple Slack Teams  
**Recurrence & Smart Suggestions** Handles recurring meetings with adaptive context aware logic  
**Federated Privacy** Schedules collaboratively without exposing private data  
**Voice & Multimodal Interfaces** Speak type or tap OASIS will understand  
**Multi Agent Negotiation** OASIS agents can negotiate between orgs projects and external partners for seamless coordination

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

## 💬 Acknowledgements

Grateful for the inspiration and support from **AMDAI Hackathon Team** and **E Cell IIT Mumbai**  
Thank you for pushing us to build the future together

## 🤝 Join the Revolution

OASIS is open for collaboration feedback and contributions  
Raise an issue star the repo and help us build the next era of agentic AI

> **OASIS isn’t just a scheduling tool. It’s the dawn of intelligent context driven collaboration. Welcome to the future.**
