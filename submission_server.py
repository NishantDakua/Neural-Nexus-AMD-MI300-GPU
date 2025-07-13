

import asyncio
import aiohttp
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Import everything from your original code
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import pytz
import json
from openai import OpenAI
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from flask import Flask, request, jsonify, render_template_string
from threading import Thread

# ADDED: Global metrics tracking (ONLY ADDITION - no logic changes)
metrics = {
    'total_requests': 0,
    'successful_requests': 0,
    'failed_requests': 0,
    'processing_times': [],
    'recent_requests': [],
    'timezone_conflicts': 0,
    'ai_fallbacks': 0,
    'start_time': datetime.now(),
    'ai_success_rate': 0,
    'average_processing_time': 0
}

# FIXED: Your original configurations with corrected token loading
def load_employee_tokens():
    """FIXED: Corrected token path construction"""
    employee_emails = [
        "userone.amd@gmail.com",
        "usertwo.amd@gmail.com", 
        "userthree.amd@gmail.com"
    ]
    
    tokens = {}
    for email in employee_emails:
        try:
            username = email.split("@")[0]  # This gives "userone.amd", "usertwo.amd", etc.
            token_path = f"Keys/{username}.token"  # FIXED: Removed duplicate .amd
            
            with open(token_path, 'r') as f:
                token_data = json.load(f)
            
            tokens[email] = token_data
            print(f"Loaded token for {email}")
            
        except Exception as e:
            print(f"Failed to load token for {email}: {e}")
    
    return tokens

EMPLOYEE_TOKENS = load_employee_tokens()
AI_BASE_URL = "http://localhost:3000/v1"
AI_MODEL = "/home/user/Models/deepseek-ai/deepseek-llm-7b-chat"

# EXACT SAME TimezoneVerificationAgent (no AI calls anyway)
class TimezoneVerificationAgent:
    """EXACT COPY of your original"""
    def __init__(self):
        pass

    def verify_timezone_compatibility(self, proposed_time: str, employee_agents: Dict) -> Dict:
        """EXACT SAME logic as your original"""
        timezone_assignments = {
            "userone.amd@gmail.com": "Asia/Kolkata",
            "usertwo.amd@gmail.com": "America/New_York",
            "userthree.amd@gmail.com": "Asia/Kolkata"
        }
        
        try:
            ist_tz = pytz.timezone('Asia/Kolkata')
            proposed_dt = datetime.fromisoformat(proposed_time.replace('+05:30', ''))
            proposed_dt = ist_tz.localize(proposed_dt)
            
            timezone_conflicts = []
            compatible_count = 0
            
            for email, timezone_name in timezone_assignments.items():
                try:
                    employee_tz = pytz.timezone(timezone_name)
                    local_time = proposed_dt.astimezone(employee_tz)
                    
                    hour = local_time.hour
                    if hour < 9 or hour >= 18:
                        timezone_conflicts.append({
                            "agent": email,
                            "timezone": timezone_name,
                            "local_time": local_time.strftime("%I:%M %p"),
                            "issue": f"Outside business hours ({hour}:00)"
                        })
                    else:
                        compatible_count += 1
                        
                except Exception as e:
                    print(f"Error checking timezone for {email}: {e}")
                    timezone_conflicts.append({
                        "agent": email,
                        "timezone": timezone_name,
                        "local_time": "Unknown",
                        "issue": f"Timezone error: {str(e)}"
                    })
            
            is_compatible = len(timezone_conflicts) == 0
            
            suggested_alternative = proposed_time
            if not is_compatible:
                suggested_dt = proposed_dt.replace(hour=16, minute=0)
                suggested_alternative = suggested_dt.strftime('%Y-%m-%dT%H:%M:%S+05:30')
            
            return {
                "compatible": is_compatible,
                "timezone_conflicts": timezone_conflicts,
                "suggested_alternative": suggested_alternative,
                "timezone_summary": f"{compatible_count} agents compatible, {len(timezone_conflicts)} agents have conflicts",
                "recommendation": "Proceed with scheduling" if is_compatible else "Reschedule to suggested time",
                "timezone_assignments": timezone_assignments,
                "verification_method": "Direct timezone calculation"
            }
            
        except Exception as e:
            print(f"Direct timezone verification failed: {e}")
            return {
                "compatible": True,
                "timezone_conflicts": [],
                "suggested_alternative": proposed_time,
                "timezone_summary": "Fallback: Assuming compatible",
                "recommendation": "Proceed with scheduling",
                "timezone_assignments": timezone_assignments,
                "verification_method": "Ultimate fallback"
            }

# EXACT SAME MeetingParserAgent with YOUR AI logic
class MeetingParserAgent:
    """EXACT COPY of your original with SAME system prompt"""
    def __init__(self):
        self.ai_client = OpenAI(api_key="NULL", base_url=AI_BASE_URL)
        # YOUR EXACT SYSTEM PROMPT
        self.system_prompt = """Parse meeting requests. Extract duration, urgency, datetime. Return JSON: {"duration_minutes":30,"urgency":"medium","preferred_datetime":"2025-07-03T14:00:00+05:30"}"""

    def parse_request(self, email_content: str, request_datetime: str) -> Dict:
        """EXACT SAME AI logic as your original"""
        base_date = datetime.strptime(request_datetime, '%d-%m-%YT%H:%M:%S')
        user_prompt = f"Parse: {email_content}. Date: {base_date.strftime('%Y-%m-%d')}."

        try:
            # YOUR EXACT AI CALL
            response = self.ai_client.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=50
            )
            
            result = response.choices[0].message.content.strip()
            if result:
                return json.loads(result)
            else:
                raise ValueError("Empty response")
        except Exception as e:
            print(f"MeetingParserAgent failed: {e}")
            raise e

# OPTIMIZED EmployeeAgent that preserves ALL your AI logic
class OptimizedEmployeeAgent:
    """Same AI logic as your original, just with parallel execution capability"""
    
    def __init__(self, email: str, token_info: Dict):
        self.email = email
        self.token_info = token_info
        self.calendar_service = self._init_calendar()
        self.ai_client = OpenAI(api_key="NULL", base_url=AI_BASE_URL)
        
    def _init_calendar(self):
        """EXACT SAME as your original"""
        creds = Credentials(
            token=self.token_info["token"],
            refresh_token=self.token_info["refresh_token"],
            token_uri=self.token_info["token_uri"],
            client_id=self.token_info["client_id"],
            client_secret=self.token_info["client_secret"],
            scopes=self.token_info["scopes"]
        )
        return build("calendar", "v3", credentials=creds)
    
    def get_calendar_events(self, start_time: str, end_time: str) -> List[Dict]:
        """EXACT SAME logic as your original"""
        events_result = self.calendar_service.events().list(
            calendarId='primary',
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        processed_events = []
        
        for event in events:
            attendees = []
            if 'attendees' in event:
                attendees = [a['email'] for a in event['attendees']]
            else:
                attendees = ["SELF"]
                
            processed_events.append({
                "StartTime": event['start'].get('dateTime', event['start'].get('date')),
                "EndTime": event['end'].get('dateTime', event['end'].get('date')),
                "NumAttendees": len(attendees),
                "Attendees": attendees,
                "Summary": event.get('summary', 'Busy')
            })
        
        return processed_events
    
    def find_available_slots(self, start_date: str, end_date: str, duration_mins: int) -> List[Dict]:
        """EXACT SAME AI logic as your original"""
        calendar_events = self.get_calendar_events(start_date, end_date)
        
        try:
            # YOUR EXACT logic for busy times
            busy_times = []
            for event in calendar_events:
                busy_times.append({
                    "start": event["StartTime"],
                    "end": event["EndTime"]
                })
            
            # YOUR EXACT PROMPT
            prompt = f"""Find {duration_mins}min slots between {start_date} and {end_date}. 
Busy: {json.dumps(busy_times[:10])}
Hours: 9AM-6PM weekdays.
Return JSON: [{{"start":"2025-07-17T10:00:00+05:30","end":"2025-07-17T10:30:00+05:30","score":0.9}}]"""
            
            # YOUR EXACT AI CALL
            response = self.ai_client.chat.completions.create(
                model=AI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=300
            )
            
            result = response.choices[0].message.content.strip()
            if result:
                return json.loads(result)
            else:
                raise ValueError("Empty response")
        except Exception as e:
            print(f"AI slot finding failed for {self.email}: {e}, using fallback")
            # YOUR EXACT FALLBACK LOGIC
            start_dt = datetime.fromisoformat(start_date.replace('+05:30', ''))
            slots = []
            for i in range(5):
                slot_start = start_dt.replace(hour=10 + i, minute=0)
                slot_end = slot_start + timedelta(minutes=duration_mins)
                slots.append({
                    "start": slot_start.strftime('%Y-%m-%dT%H:%M:%S+05:30'),
                    "end": slot_end.strftime('%Y-%m-%dT%H:%M:%S+05:30'),
                    "score": 0.8 - i * 0.1
                })
            return slots
    
    def negotiate_slot(self, proposed_slots: List[Dict], other_agents_proposals: List[Dict]) -> Dict:
        """EXACT SAME AI negotiation logic as your original"""
        try:
            # YOUR EXACT PROMPT
            prompt = f"""Agent {self.email} negotiation.
My slots: {json.dumps(proposed_slots[:3])}
Others: {json.dumps(other_agents_proposals[:2])}
Pick best common slot.
Return: {{"start":"...","end":"...","confidence":0.9}}"""
            
            # YOUR EXACT AI CALL
            response = self.ai_client.chat.completions.create(
                model=AI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=150
            )
            
            result = response.choices[0].message.content.strip()
            if result:
                return json.loads(result)
            else:
                raise ValueError("Empty response")
        except Exception as e:
            print(f"AI negotiation failed for {self.email}: {e}, using fallback")
            # YOUR EXACT FALLBACK LOGIC
            if proposed_slots:
                return {
                    "start": proposed_slots[0]["start"],
                    "end": proposed_slots[0]["end"],
                    "confidence": 0.7
                }
            else:
                return {
                    "start": "2025-07-17T14:00:00+05:30",
                    "end": "2025-07-17T14:30:00+05:30",
                    "confidence": 0.5
                }

# OPTIMIZED BossAgent with ALL your AI logic preserved
class OptimizedBossAgent:
    """Preserves ALL your AI logic, adds parallel execution"""
    
    def __init__(self):
        self.ai_client = OpenAI(api_key="NULL", base_url=AI_BASE_URL)
        self.employee_agents = {}
        for email, token_info in EMPLOYEE_TOKENS.items():
            self.employee_agents[email] = OptimizedEmployeeAgent(email, token_info)
        self.ist_tz = pytz.timezone('Asia/Kolkata')
        self.parser_agent = MeetingParserAgent()  # YOUR EXACT PARSER
        self.timezone_agent = TimezoneVerificationAgent()  # YOUR EXACT TIMEZONE AGENT
    
    def parse_meeting_request(self, email_content: str, request_datetime: str) -> Dict:
        """EXACT SAME logic as your original"""
        base_date = datetime.strptime(request_datetime, '%d-%m-%YT%H:%M:%S')
        
        try:
            # YOUR EXACT MeetingParserAgent call
            return self.parser_agent.parse_request(email_content, request_datetime)
        except Exception as e:
            print(f"AI parsing failed: {e}, using fallback")
            # YOUR EXACT FALLBACK LOGIC
            duration = 30
            if "45 minutes" in email_content.lower() or "45 min" in email_content.lower():
                duration = 45
            elif "hour" in email_content.lower():
                duration = 60
            
            urgency = "medium"
            if "urgent" in email_content.lower():
                urgency = "urgent"
            
            next_thursday = base_date + timedelta(days=(3 - base_date.weekday()) % 7)
            if next_thursday <= base_date:
                next_thursday += timedelta(days=7)
            
            return {
                "duration_minutes": duration,
                "urgency": urgency,
                "preferred_datetime": next_thursday.strftime('%Y-%m-%dT14:00:00+05:30')
            }
    
    def coordinate_scheduling_parallel(self, participants: List[str], meeting_info: Dict) -> Dict:
        """SAME coordination logic with parallel execution"""
        
        # YOUR EXACT time window calculation
        if meeting_info.get('preferred_datetime'):
            start_date = datetime.fromisoformat(meeting_info['preferred_datetime'].replace('+05:30', ''))
        else:
            start_date = datetime.now(self.ist_tz) + timedelta(days=1)
        
        search_days = {'urgent': 3, 'high': 7, 'medium': 14, 'low': 21}
        end_date = start_date + timedelta(days=search_days.get(meeting_info['urgency'], 14))
        
        start_str = start_date.strftime('%Y-%m-%dT00:00:00+05:30')
        end_str = end_date.strftime('%Y-%m-%dT23:59:59+05:30')
        
        # YOUR EXACT timezone verification
        proposed_time = meeting_info.get('preferred_datetime', start_str)
        print(f"🔍 Timezone verification for proposed time: {proposed_time}")
        timezone_verification = self.timezone_agent.verify_timezone_compatibility(
            proposed_time, self.employee_agents
        )
        print(f"🔍 Timezone verification result: {json.dumps(timezone_verification, indent=2)}")
        
        # YOUR EXACT timezone handling
        if not timezone_verification.get('compatible', True):
            suggested_time = timezone_verification.get('suggested_alternative', proposed_time)
            print(f"Timezone conflict detected. Using suggested time: {suggested_time}")
            meeting_info['preferred_datetime'] = suggested_time
            start_date = datetime.fromisoformat(suggested_time.replace('+05:30', ''))
            start_str = start_date.strftime('%Y-%m-%dT00:00:00+05:30')
            end_str = (start_date + timedelta(days=search_days.get(meeting_info['urgency'], 14))).strftime('%Y-%m-%dT23:59:59+05:30')
        
        # ONLY OPTIMIZATION: Parallel execution of YOUR EXACT AI logic
        # Phase 1: Parallel slot finding with YOUR EXACT AI calls
        def find_slots_for_participant(participant):
            if participant in self.employee_agents:
                agent = self.employee_agents[participant]
                # YOUR EXACT AI slot finding call
                slots = agent.find_available_slots(start_str, end_str, meeting_info['duration_minutes'])
                return participant, slots
            return participant, []
        
        # Execute YOUR AI calls in parallel
        all_proposals = {}
        with ThreadPoolExecutor(max_workers=len(participants)) as executor:
            futures = [executor.submit(find_slots_for_participant, p) for p in participants]
            for future in as_completed(futures):
                participant, slots = future.result()
                all_proposals[participant] = slots
        
        # Phase 2: Parallel negotiation with YOUR EXACT AI calls
        def negotiate_for_participant(participant):
            if participant in self.employee_agents:
                agent = self.employee_agents[participant]
                other_proposals = [slots[:3] for email, slots in all_proposals.items() if email != participant]
                # YOUR EXACT AI negotiation call
                result = agent.negotiate_slot(all_proposals[participant], other_proposals)
                return result
            return {}
        
        # Execute YOUR AI negotiations in parallel
        negotiation_results = []
        with ThreadPoolExecutor(max_workers=len(participants)) as executor:
            futures = [executor.submit(negotiate_for_participant, p) for p in participants]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    negotiation_results.append(result)
        
        # Phase 3: YOUR EXACT boss decision
        final_decision = self.make_final_decision(negotiation_results, meeting_info)
        final_decision['timezone_verification'] = timezone_verification
        
        return final_decision
    
    def make_final_decision(self, negotiation_results: List[Dict], meeting_info: Dict) -> Dict:
        """EXACT SAME boss AI logic as your original"""
        try:
            # YOUR EXACT PROMPT
            prompt = f"""Boss final decision.
Duration: {meeting_info['duration_minutes']}mins
Urgency: {meeting_info['urgency']}
Results: {json.dumps(negotiation_results[:3])}

Pick best time with highest consensus.
Return: {{"start":"2025-07-17T14:00:00+05:30","end":"2025-07-17T14:30:00+05:30","confidence":0.95}}"""
            
            # YOUR EXACT AI CALL
            response = self.ai_client.chat.completions.create(
                model=AI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=150
            )
            
            result = response.choices[0].message.content.strip()
            if result:
                return json.loads(result)
            else:
                raise ValueError("Empty response")
        except Exception as e:
            print(f"AI final decision failed: {e}, using fallback")
            # YOUR EXACT FALLBACK LOGIC
            if negotiation_results:
                best_result = max(negotiation_results, key=lambda x: x.get('confidence', 0))
                return {
                    "start": best_result["start"],
                    "end": best_result["end"],
                    "confidence": best_result.get("confidence", 0.7)
                }
            else:
                preferred_dt = meeting_info.get('preferred_datetime', '2025-07-17T14:00:00+05:30')
                start_dt = datetime.fromisoformat(preferred_dt.replace('+05:30', ''))
                end_dt = start_dt + timedelta(minutes=meeting_info['duration_minutes'])
                return {
                    "start": start_dt.strftime('%Y-%m-%dT%H:%M:%S+05:30'),
                    "end": end_dt.strftime('%Y-%m-%dT%H:%M:%S+05:30'),
                    "confidence": 0.6
                }

def optimized_your_meeting_assistant(data):
    """EXACT SAME logic flow as your original, just parallel execution"""
    try:
        start_time = time.time()
        
        # Use optimized boss agent (preserves ALL your AI)
        boss = OptimizedBossAgent()
        
        # YOUR EXACT parsing step
        meeting_info = boss.parse_meeting_request(
            data['EmailContent'],
            data['Datetime']
        )
        
        # YOUR EXACT participant logic
        all_participants = [data['From']] + [a['email'] for a in data['Attendees']]
        
        # YOUR EXACT coordination with parallel optimization
        scheduled_meeting = boss.coordinate_scheduling_parallel(all_participants, meeting_info)
        
        # YOUR EXACT output building
        search_date = datetime.fromisoformat(scheduled_meeting['start'].replace('+05:30', ''))
        day_start = search_date.strftime('%Y-%m-%dT00:00:00+05:30')
        day_end = search_date.strftime('%Y-%m-%dT23:59:59+05:30')
        
        # Parallel calendar fetching for output (only optimization here)
        def get_events_for_participant(participant):
            events = []
            if participant in boss.employee_agents:
                events = boss.employee_agents[participant].get_calendar_events(day_start, day_end)
            
            # YOUR EXACT new meeting addition
            events.append({
                "StartTime": scheduled_meeting['start'],
                "EndTime": scheduled_meeting['end'],
                "NumAttendees": len(all_participants),
                "Attendees": all_participants,
                "Summary": data.get('Subject', 'Meeting')
            })
            
            return {
                "email": participant,
                "events": events
            }
        
        # Execute calendar fetching in parallel
        attendees_with_events = []
        with ThreadPoolExecutor(max_workers=len(all_participants)) as executor:
            futures = [executor.submit(get_events_for_participant, p) for p in all_participants]
            for future in as_completed(futures):
                attendees_with_events.append(future.result())
        
        # YOUR EXACT output format
        output = {
            "Request_id": data['Request_id'],
            "Datetime": data['Datetime'],
            "Location": data['Location'],
            "From": data['From'],
            "Attendees": attendees_with_events,
            "Subject": data['Subject'],
            "EmailContent": data['EmailContent'],
            "EventStart": scheduled_meeting['start'],
            "EventEnd": scheduled_meeting['end'],
            "Duration_mins": str(meeting_info['duration_minutes']),
            "MetaData": {
                "timezone_verification": scheduled_meeting.get('timezone_verification', {}),
                "timezone_summary": scheduled_meeting.get('timezone_verification', {}).get('timezone_summary', 'All agents in same timezone'),
                "timezone_assignments": scheduled_meeting.get('timezone_verification', {}).get('timezone_assignments', {}),
                "scheduling_step": "Boss Agent verified timezone compatibility before scheduling",
                "processing_time_seconds": round(time.time() - start_time, 2),
                "optimization": "Parallel execution of original AI logic"
            }
        }
        
        # YOUR EXACT processed format
        processed = {
            "Request_id": data['Request_id'],
            "Datetime": data['Datetime'],
            "Location": data['Location'],
            "From": data['From'],
            "Attendees": data['Attendees'],
            "Subject": data['Subject'],
            "EmailContent": data['EmailContent'],
            "Start": scheduled_meeting['start'],
            "End": scheduled_meeting['end'],
            "Duration_mins": str(meeting_info['duration_minutes'])
        }
        
        data["processed"] = processed
        data["output"] = output
        
        return data
        
    except Exception as e:
        print(f"Error: {e}")
        data["processed"] = {"error": str(e)}
        data["output"] = {"error": str(e)}
        return data

# Flask server with optimized function
app = Flask(__name__)
received_data = []

# ADDED: Dashboard routes (NEW - no changes to existing logic)
@app.route('/')
def dashboard():
    """Beautiful dashboard UI"""
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 AI Meeting Assistant Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }
        
        .header h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 45px rgba(0,0,0,0.2);
        }
        
        .card-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .card-icon {
            font-size: 2rem;
            margin-right: 15px;
        }
        
        .card-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #555;
        }
        
        .card-value {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .card-subtitle {
            font-size: 0.9rem;
            color: #777;
        }
        
        .success { color: #27ae60; }
        .warning { color: #f39c12; }
        .error { color: #e74c3c; }
        .info { color: #3498db; }
        .primary { color: #667eea; }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        
        .status-online { background-color: #27ae60; }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .recent-requests {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .requests-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .request-item {
            padding: 15px;
            border-left: 4px solid #667eea;
            margin-bottom: 10px;
            background: rgba(102, 126, 234, 0.05);
            border-radius: 8px;
        }
        
        .request-time {
            font-size: 0.8rem;
            color: #777;
            margin-bottom: 5px;
        }
        
        .request-details {
            font-weight: 500;
        }
        
        .progress-bar {
            width: 100%;
            height: 10px;
            background: #ecf0f1;
            border-radius: 5px;
            overflow: hidden;
            margin-top: 10px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 5px;
            transition: width 0.5s ease;
        }
        
        .test-section {
            margin-top: 40px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        .test-button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: transform 0.2s ease;
        }
        
        .test-button:hover {
            transform: scale(1.05);
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            color: rgba(255,255,255,0.8);
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Meeting Assistant</h1>
            <p><span class="status-indicator status-online"></span>System Running on Port 5000</p>
        </div>
        
        <div class="cards-grid">
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">📊</div>
                    <div class="card-title">Total Requests</div>
                </div>
                <div class="card-value info" id="total-requests">0</div>
                <div class="card-subtitle">Meeting requests processed</div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">✅</div>
                    <div class="card-title">Success Rate</div>
                </div>
                <div class="card-value success" id="success-rate">100%</div>
                <div class="progress-bar">
                    <div class="progress-fill" id="success-progress" style="width: 100%"></div>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">⚡</div>
                    <div class="card-title">Avg Processing Time</div>
                </div>
                <div class="card-value primary" id="avg-time">0.0s</div>
                <div class="card-subtitle">Response time per request</div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">🌍</div>
                    <div class="card-title">Timezone Conflicts</div>
                </div>
                <div class="card-value warning" id="timezone-conflicts">0</div>
                <div class="card-subtitle">Detected scheduling conflicts</div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">🤖</div>
                    <div class="card-title">AI Success Rate</div>
                </div>
                <div class="card-value info" id="ai-success">100%</div>
                <div class="card-subtitle">AI vs Fallback usage</div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">⏰</div>
                    <div class="card-title">System Uptime</div>
                </div>
                <div class="card-value primary" id="uptime">0m</div>
                <div class="card-subtitle">Since last restart</div>
            </div>
        </div>
        
        <div class="recent-requests">
            <div class="requests-header">
                <div class="card-icon">📋</div>
                <h3>Recent Meeting Requests</h3>
            </div>
            <div id="recent-requests-list">
                <div class="request-item">
                    <div class="request-time">Waiting for first request...</div>
                    <div class="request-details">System ready to process meeting requests</div>
                </div>
            </div>
        </div>
        
        <div class="test-section">
            <h3>🧪 Quick Test</h3>
            <p style="margin: 15px 0;">Test your API endpoint with a sample request:</p>
            <button class="test-button" onclick="runTest()">Run Test Request</button>
            <div id="test-result" style="margin-top: 15px;"></div>
        </div>
        
        <div class="footer">
            <p>🚀 Optimized AI Meeting Assistant with Parallel Processing | Port Forwarded Dashboard</p>
        </div>
    </div>

    <script>
        // Auto-refresh data every 5 seconds
        setInterval(updateDashboard, 5000);
        updateDashboard(); // Initial load
        
        async function updateDashboard() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                
                // Update cards
                document.getElementById('total-requests').textContent = data.total_requests;
                document.getElementById('success-rate').textContent = data.success_rate + '%';
                document.getElementById('avg-time').textContent = data.average_processing_time + 's';
                document.getElementById('timezone-conflicts').textContent = data.timezone_conflicts;
                document.getElementById('ai-success').textContent = data.ai_success_rate + '%';
                document.getElementById('uptime').textContent = data.uptime;
                
                // Update progress bar
                document.getElementById('success-progress').style.width = data.success_rate + '%';
                
                // Update recent requests
                updateRecentRequests(data.recent_requests);
                
            } catch (error) {
                console.log('Dashboard update failed:', error);
            }
        }
        
        function updateRecentRequests(requests) {
            const container = document.getElementById('recent-requests-list');
            if (requests.length === 0) return;
            
            container.innerHTML = requests.map(req => `
                <div class="request-item">
                    <div class="request-time">${req.time}</div>
                    <div class="request-details">
                        ${req.from} → ${req.subject} (${req.duration}min, ${req.processing_time}s)
                        ${req.success ? '✅' : '❌'}
                    </div>
                </div>
            `).join('');
        }
        
        async function runTest() {
            const testData = {
                "Request_id": "dashboard_test_" + Date.now(),
                "Datetime": "13-07-2025T14:00:00",
                "Location": "Dashboard Test",
                "From": "userone.amd@gmail.com",
                "Attendees": [{"email": "usertwo.amd@gmail.com"}],
                "Subject": "Dashboard Test Meeting",
                "EmailContent": "Quick 30 minute test from dashboard"
            };
            
            document.getElementById('test-result').innerHTML = '🔄 Running test...';
            
            try {
                const response = await fetch('/receive', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(testData)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    document.getElementById('test-result').innerHTML = `
                        <div style="color: #27ae60; margin-top: 10px;">
                            ✅ Test Successful!<br>
                            📅 Scheduled: ${result.EventStart} to ${result.EventEnd}<br>
                            ⚡ Processing Time: ${result.MetaData?.processing_time_seconds}s
                        </div>
                    `;
                } else {
                    document.getElementById('test-result').innerHTML = `
                        <div style="color: #e74c3c; margin-top: 10px;">
                            ❌ Test Failed: ${JSON.stringify(result)}
                        </div>
                    `;
                }
                
                // Refresh dashboard after test
                setTimeout(updateDashboard, 1000);
                
            } catch (error) {
                document.getElementById('test-result').innerHTML = `
                    <div style="color: #e74c3c; margin-top: 10px;">
                        ❌ Test Error: ${error.message}
                    </div>
                `;
            }
        }
    </script>
</body>
</html>
    """
    return render_template_string(html_template)

@app.route('/api/stats')
def get_stats():
    """API endpoint for dashboard statistics"""
    # Calculate uptime
    uptime_delta = datetime.now() - metrics['start_time']
    uptime_str = f"{uptime_delta.days}d {uptime_delta.seconds//3600}h {(uptime_delta.seconds//60)%60}m"
    if uptime_delta.total_seconds() < 3600:  # Less than 1 hour
        uptime_str = f"{(uptime_delta.seconds//60)%60}m {uptime_delta.seconds%60}s"
    
    # Calculate success rate
    total = metrics['total_requests']
    success_rate = (metrics['successful_requests'] / total * 100) if total > 0 else 100
    
    # Calculate AI success rate
    ai_attempts = total - metrics['ai_fallbacks']
    ai_success_rate = (ai_attempts / total * 100) if total > 0 else 100
    
    # Calculate average processing time
    avg_time = sum(metrics['processing_times']) / len(metrics['processing_times']) if metrics['processing_times'] else 0
    
    return jsonify({
        'total_requests': metrics['total_requests'],
        'successful_requests': metrics['successful_requests'],
        'failed_requests': metrics['failed_requests'],
        'success_rate': round(success_rate, 1),
        'ai_success_rate': round(ai_success_rate, 1),
        'average_processing_time': round(avg_time, 2),
        'timezone_conflicts': metrics['timezone_conflicts'],
        'ai_fallbacks': metrics['ai_fallbacks'],
        'uptime': uptime_str,
        'recent_requests': metrics['recent_requests'][-10:]  # Last 10 requests
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'tokens_loaded': len(EMPLOYEE_TOKENS),
        'ai_server': AI_BASE_URL
    })

@app.route('/receive', methods=['POST'])
def receive_optimized():
    data = request.get_json()
    print(f"\n🚀 OPTIMIZED: Received meeting request (preserving ALL AI logic)")
    
    # ADDED: Track request start (ONLY metrics addition)
    start_time = time.time()
    metrics['total_requests'] += 1
    
    processed_data = optimized_your_meeting_assistant(data)
    received_data.append(data)
    
    # ADDED: Track request completion (ONLY metrics addition)
    processing_time = time.time() - start_time
    metrics['processing_times'].append(processing_time)
    
    if 'error' not in processed_data.get('output', {}):
        metrics['successful_requests'] += 1
        
        # Track timezone conflicts
        tz_verification = processed_data.get('output', {}).get('MetaData', {}).get('timezone_verification', {})
        if not tz_verification.get('compatible', True):
            metrics['timezone_conflicts'] += 1
        
        # Add to recent requests
        metrics['recent_requests'].append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'from': data.get('From', 'Unknown'),
            'subject': data.get('Subject', 'No Subject'),
            'duration': processed_data.get('output', {}).get('Duration_mins', 'Unknown'),
            'processing_time': round(processing_time, 2),
            'success': True
        })
    else:
        metrics['failed_requests'] += 1
        metrics['recent_requests'].append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'from': data.get('From', 'Unknown'),
            'subject': data.get('Subject', 'No Subject'),
            'duration': 'Failed',
            'processing_time': round(processing_time, 2),
            'success': False
        })
    
    print(f"\n⚡ PERFORMANCE: {processed_data['output'].get('MetaData', {}).get('processing_time_seconds', 'N/A')}s with ALL AI preserved")
    
    response = app.response_class(
        response=json.dumps(processed_data['output'], indent=2, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )
    return response

def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    run_flask()
