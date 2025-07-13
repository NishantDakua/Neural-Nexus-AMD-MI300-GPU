#!/usr/bin/env python3
"""
TRUE preservation of your original AI logic with ONLY execution optimization
EVERY AI call, prompt, and logic flow preserved 100%
"""

import asyncio
import aiohttp
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import everything from your original code
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import pytz
import json
from openai import OpenAI
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from flask import Flask, request, jsonify
from threading import Thread

# Your EXACT original configurations
def load_employee_tokens():
    """EXACT SAME as your original"""
    employee_emails = [
        "userone.amd@gmail.com",
        "usertwo.amd@gmail.com", 
        "userthree.amd@gmail.com"
    ]
    
    tokens = {}
    for email in employee_emails:
        try:
            username = email.split("@")[0]
            token_base_path = os.getenv("TOKEN_BASE_PATH")
            token_path = f"{token_base_path}/{username}.amd.token"
            
            with open(token_path, 'r') as f:
                token_data = json.load(f)
            
            tokens[email] = token_data
            print(f"Loaded token for {email}")
            
        except Exception as e:
            print(f"Failed to load token for {email}: {e}")
    
    return tokens

EMPLOYEE_TOKENS = load_employee_tokens()
AI_BASE_URL = os.getenv("AI_BASE_URL")
AI_MODEL = os.getenv("AI_MODEL")

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
            default_timezone = os.getenv("DEFAULT_TIMEZONE")
            ist_tz = pytz.timezone(default_timezone)
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

@app.route('/receive', methods=['POST'])
def receive_optimized():
    data = request.get_json()
    print(f"\n🚀 OPTIMIZED: Received meeting request (preserving ALL AI logic)")
    processed_data = optimized_your_meeting_assistant(data)
    received_data.append(data)
    print(f"\n⚡ PERFORMANCE: {processed_data['output'].get('MetaData', {}).get('processing_time_seconds', 'N/A')}s with ALL AI preserved")
    
    response = app.response_class(
        response=json.dumps(processed_data['output'], indent=2, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )
    return response

def run_flask():
    host = os.getenv("FLASK_HOST")
    port = int(os.getenv("FLASK_PORT"))
    debug = os.getenv("FLASK_DEBUG").lower() == "true"
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    run_flask()
