#!/usr/import json
import re
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import pytz
from dataclasses import dataclass
from openai import OpenAI
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import time
from flask import Flask, request, jsonify
from threading import Thread
from dotenv import load_dotenvon3
"""
AI Scheduling Assistant with Boss-Employee Agent Architecture
Real Google Calendar Integration + A2A Communication
"""

import json
import re
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import pytz
from dataclasses import dataclass
from openai import OpenAI
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import time
from flask import Flask, request, jsonify
from threading import Thread
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build employee tokens from environment variables
def build_employee_tokens():
    """Build employee tokens dictionary from environment variables"""
    tokens = {}
    
    # Employee 1
    email1 = os.getenv('EMPLOYEE1_EMAIL')
    if email1:
        tokens[email1] = {
            "token": os.getenv('EMPLOYEE1_TOKEN'),
            "refresh_token": os.getenv('EMPLOYEE1_REFRESH_TOKEN'),
            "token_uri": os.getenv('GOOGLE_TOKEN_URI'),
            "client_id": os.getenv('EMPLOYEE1_CLIENT_ID'),
            "client_secret": os.getenv('EMPLOYEE1_CLIENT_SECRET'),
            "scopes": [os.getenv('GOOGLE_SCOPES')]
        }
    
    # Employee 2
    email2 = os.getenv('EMPLOYEE2_EMAIL')
    if email2:
        tokens[email2] = {
            "token": os.getenv('EMPLOYEE2_TOKEN'),
            "refresh_token": os.getenv('EMPLOYEE2_REFRESH_TOKEN'),
            "token_uri": os.getenv('GOOGLE_TOKEN_URI'),
            "client_id": os.getenv('EMPLOYEE2_CLIENT_ID'),
            "client_secret": os.getenv('EMPLOYEE2_CLIENT_SECRET'),
            "scopes": [os.getenv('GOOGLE_SCOPES')]
        }
    
    # Employee 3
    email3 = os.getenv('EMPLOYEE3_EMAIL')
    if email3:
        tokens[email3] = {
            "token": os.getenv('EMPLOYEE3_TOKEN'),
            "refresh_token": os.getenv('EMPLOYEE3_REFRESH_TOKEN'),
            "token_uri": os.getenv('GOOGLE_TOKEN_URI'),
            "client_id": os.getenv('EMPLOYEE3_CLIENT_ID'),
            "client_secret": os.getenv('EMPLOYEE3_CLIENT_SECRET'),
            "scopes": [os.getenv('GOOGLE_SCOPES')]
        }
    
    return tokens

# Employee tokens from environment variables
EMPLOYEE_TOKENS = build_employee_tokens()

# AI Configuration from environment variables
AI_BASE_URL = os.getenv('AI_BASE_URL', 'http://localhost:3000/v1')
AI_MODEL = os.getenv('AI_MODEL', '/home/user/Models/deepseek-ai/deepseek-llm-7b-chat')

class EmployeeAgent:
    """Employee Agent with Google Calendar access and AI capabilities"""
    
    def __init__(self, email: str, token_info: Dict):
        self.email = email
        self.token_info = token_info
        self.calendar_service = self._init_calendar()
        self.ai_client = OpenAI(api_key="NULL", base_url=AI_BASE_URL)
        
    def _init_calendar(self):
        """Initialize Google Calendar connection"""
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
        """Fetch real calendar events"""
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
        """AI-powered slot finding with fallback"""
        calendar_events = self.get_calendar_events(start_date, end_date)
        
        try:
            # Create concise event summary to avoid token limit
            busy_times = []
            for event in calendar_events:
                busy_times.append({
                    "start": event["StartTime"],
                    "end": event["EndTime"]
                })
            
            prompt = f"""Find {duration_mins}min slots between {start_date} and {end_date}. 
Busy: {json.dumps(busy_times[:10])}
Hours: 9AM-6PM weekdays.
Return JSON: [{{"start":"2025-07-17T10:00:00+05:30","end":"2025-07-17T10:30:00+05:30","score":0.9}}]"""
            
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
            # Simple fallback - generate basic slots
            start_dt = datetime.fromisoformat(start_date.replace('+05:30', ''))
            slots = []
            for i in range(5):  # Generate 5 potential slots
                slot_start = start_dt.replace(hour=10 + i, minute=0)
                slot_end = slot_start + timedelta(minutes=duration_mins)
                slots.append({
                    "start": slot_start.strftime('%Y-%m-%dT%H:%M:%S+05:30'),
                    "end": slot_end.strftime('%Y-%m-%dT%H:%M:%S+05:30'),
                    "score": 0.8 - i * 0.1
                })
            return slots
    
    def negotiate_slot(self, proposed_slots: List[Dict], other_agents_proposals: List[Dict]) -> Dict:
        """A2A negotiation with other agents with fallback"""
        try:
            prompt = f"""Agent {self.email} negotiation.
My slots: {json.dumps(proposed_slots[:3])}
Others: {json.dumps(other_agents_proposals[:2])}
Pick best common slot.
Return: {{"start":"...","end":"...","confidence":0.9}}"""
            
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
            # Fallback - pick first available slot
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

class TimezoneVerificationAgent:
    """AI Agent for timezone compatibility verification between Boss and Employee Agents"""
    
    def __init__(self):
        self.ai_client = OpenAI(api_key="NULL", base_url=AI_BASE_URL)
        self.system_prompt = """You are a timezone compatibility verification agent. Your job is to check if a meeting time works for all participants across different timezones.

TIMEZONE ASSIGNMENTS:
- userone.amd@gmail.com: Asia/Kolkata (IST, +05:30)
- usertwo.amd@gmail.com: America/New_York (EST, -05:00)
- userthree.amd@gmail.com: Asia/Kolkata (IST, +05:30)

BUSINESS HOURS: 9 AM - 6 PM in each timezone

EXAMPLE CALCULATIONS:
- 2:00 PM IST = 4:30 AM EST (New York) = OUTSIDE business hours
- 10:00 AM IST = 12:30 AM EST (New York) = OUTSIDE business hours
- 4:00 PM IST = 6:30 AM EST (New York) = OUTSIDE business hours

TASK: Given a proposed meeting time in IST, check if it works for all timezones.

Return ONLY this JSON format:
{
    "compatible": true/false,
    "timezone_conflicts": [
        {
            "agent": "usertwo.amd@gmail.com",
            "timezone": "America/New_York", 
            "local_time": "04:30 AM",
            "issue": "Outside business hours (4:30 AM)"
        }
    ],
    "suggested_alternative": "2025-07-03T16:00:00+05:30",
    "timezone_summary": "1 agent compatible, 1 agent has conflict",
    "recommendation": "Proceed with scheduling" or "Reschedule to suggested time"
}"""

    def verify_timezone_compatibility(self, proposed_time: str, employee_agents: Dict) -> Dict:
        """Verify timezone compatibility for all employee agents using direct calculation"""
        
        # Assign different timezones to employee agents for testing
        timezone_assignments = {
            "userone.amd@gmail.com": "Asia/Kolkata",      # Same as Boss (IST)
            "usertwo.amd@gmail.com": "America/New_York",  # Different timezone
            "userthree.amd@gmail.com": "Asia/Kolkata"     # Same as Boss (IST)
        }
        
        try:
            # Parse the proposed time
            if '+05:30' in proposed_time:
                ist_time = datetime.fromisoformat(proposed_time.replace('+05:30', ''))
            else:
                ist_time = datetime.fromisoformat(proposed_time)
            
            # Define timezones
            ist_tz = pytz.timezone('Asia/Kolkata')
            est_tz = pytz.timezone('America/New_York')
            
            # Convert IST time to timezone-aware datetime
            ist_aware = ist_tz.localize(ist_time)
            
            conflicts = []
            compatible_count = 0
            
            # Check each agent's timezone
            for email, tz_name in timezone_assignments.items():
                if tz_name == "Asia/Kolkata":
                    # Same timezone as proposed time
                    local_time = ist_time
                    local_hour = local_time.hour
                    
                    if 9 <= local_hour <= 18:  # Business hours 9 AM - 6 PM
                        compatible_count += 1
                    else:
                        conflicts.append({
                            "agent": email,
                            "timezone": tz_name,
                            "local_time": local_time.strftime("%I:%M %p"),
                            "issue": f"Outside business hours ({local_time.strftime('%I:%M %p')})"
                        })
                        
                elif tz_name == "America/New_York":
                    # Convert IST to EST
                    est_time = ist_aware.astimezone(est_tz)
                    local_hour = est_time.hour
                    
                    if 9 <= local_hour <= 18:  # Business hours 9 AM - 6 PM
                        compatible_count += 1
                    else:
                        conflicts.append({
                            "agent": email,
                            "timezone": tz_name,
                            "local_time": est_time.strftime("%I:%M %p"),
                            "issue": f"Outside business hours ({est_time.strftime('%I:%M %p')} EST)"
                        })
            
            # Determine compatibility
            is_compatible = len(conflicts) == 0
            
            # Generate suggested alternative if there are conflicts
            suggested_alternative = proposed_time
            if not is_compatible:
                # Suggest 2:00 PM IST (8:30 AM EST) which works for both timezones
                suggested_time = ist_time.replace(hour=14, minute=0, second=0)
                suggested_alternative = suggested_time.strftime('%Y-%m-%dT%H:%M:%S+05:30')
            
            return {
                "compatible": is_compatible,
                "timezone_conflicts": conflicts,
                "suggested_alternative": suggested_alternative,
                "timezone_summary": f"{compatible_count} agents compatible, {len(conflicts)} agents have conflicts",
                "recommendation": "Proceed with scheduling" if is_compatible else "Reschedule to suggested time",
                "timezone_assignments": timezone_assignments
            }
            
        except Exception as e:
            print(f"TimezoneVerificationAgent calculation failed: {e}")
            # Fallback: assume compatible
            return {
                "compatible": True,
                "timezone_conflicts": [],
                "suggested_alternative": proposed_time,
                "timezone_summary": "Fallback: Assuming compatible due to calculation error",
                "recommendation": "Proceed with scheduling",
                "timezone_assignments": timezone_assignments
            }

class MeetingParserAgent:
    """AI Agent specifically for parsing meeting requests with enhanced system prompt"""
    
    def __init__(self):
        self.ai_client = OpenAI(api_key="NULL", base_url=AI_BASE_URL)
        self.system_prompt = """You are an expert meeting request parser with dynamic date/time extraction capabilities.

CORE PRINCIPLES:
1. Be DYNAMIC - handle ANY date/time expression naturally
2. Use context from current date intelligently
3. Extract duration from ANY format (minutes, hours, etc.)
4. Detect urgency from ANY expression
5. Always return valid JSON in specified format

CONTEXT AWARENESS:
- Current date context helps interpret relative dates
- "next" vs "this" week depends on current day
- Time expressions should be converted to IST (+05:30)
- Default to 14:00 if no specific time mentioned

DURATION EXTRACTION:
- Extract from ANY format: "2 hours", "90 minutes", "1.5 hours", "quarter hour"
- Convert to minutes for consistency
- Default to 30 minutes if not specified

URGENCY DETECTION:
- Look for ANY urgency indicators: "urgent", "asap", "important", "when convenient", "flexible"
- Map to: urgent, high, medium, low
- Default to medium

OUTPUT FORMAT:
Return ONLY valid JSON:
{
    "duration_minutes": <extracted_duration_in_minutes>,
    "urgency": "<urgency_level>",
    "preferred_datetime": "<YYYY-MM-DDTHH:MM:SS+05:30>"
}

BE DYNAMIC - handle any natural language date/time expression!"""

    def parse_request(self, email_content: str, request_datetime: str) -> Dict:
        """Parse meeting request using AI agent"""
        base_date = datetime.strptime(request_datetime, '%d-%m-%YT%H:%M:%S')
        
        user_prompt = f"""Parse this meeting request:

Email Content: "{email_content}"
Current Date: {base_date.strftime('%Y-%m-%d %A')}

Extract duration, urgency, and preferred datetime accurately."""

        try:
            response = self.ai_client.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=200
            )
            
            result = response.choices[0].message.content.strip()
            if result:
                return json.loads(result)
            else:
                raise ValueError("Empty response")
        except Exception as e:
            print(f"MeetingParserAgent failed: {e}")
            raise e

class BossAgent:
    """Boss Agent that coordinates scheduling between employee agents"""
    
    def __init__(self):
        # Validate environment variables are loaded
        if not EMPLOYEE_TOKENS:
            raise ValueError("No employee tokens found. Please check your .env file configuration.")
        
        print(f"✅ Loaded {len(EMPLOYEE_TOKENS)} employee tokens from environment variables")
        
        self.ai_client = OpenAI(api_key="NULL", base_url=AI_BASE_URL)
        self.employee_agents = {}
        for email, token_info in EMPLOYEE_TOKENS.items():
            self.employee_agents[email] = EmployeeAgent(email, token_info)
        self.ist_tz = pytz.timezone('Asia/Kolkata')
        self.parser_agent = MeetingParserAgent()
        self.timezone_agent = TimezoneVerificationAgent()
    
    def parse_meeting_request(self, email_content: str, request_datetime: str) -> Dict:
        """AI-powered meeting request parsing with enhanced fallback"""
        base_date = datetime.strptime(request_datetime, '%d-%m-%YT%H:%M:%S')
        
        try:
            # Use the dedicated MeetingParserAgent for better parsing
            return self.parser_agent.parse_request(email_content, request_datetime)
        except Exception as e:
            print(f"AI parsing failed: {e}, using enhanced fallback")
            
            # Enhanced fallback logic with better pattern matching
            email_lower = email_content.lower()
            
            # Duration extraction
            duration = 30  # default
            if "45 minutes" in email_lower or "45 min" in email_lower:
                duration = 45
            elif "60 minutes" in email_lower or "1 hour" in email_lower or "one hour" in email_lower:
                duration = 60
            elif "90 minutes" in email_lower or "1.5 hours" in email_lower:
                duration = 90
            elif "30 minutes" in email_lower or "30 min" in email_lower:
                duration = 30
            
            # Urgency extraction
            urgency = "medium"
            if any(word in email_lower for word in ["urgent", "asap", "emergency", "immediately"]):
                urgency = "urgent"
            elif any(word in email_lower for word in ["important", "priority", "soon"]):
                urgency = "high"
            elif any(word in email_lower for word in ["flexible", "convenient", "when possible"]):
                urgency = "low"
            
            # Time extraction with pattern matching
            preferred_datetime = None
            
            # Look for specific time patterns
            import re
            
            # Pattern: "tomorrow at X:XX AM/PM"
            tomorrow_pattern = r"tomorrow\s+at\s+(\d{1,2}):?(\d{0,2})\s*(am|pm|AM|PM)?"
            tomorrow_match = re.search(tomorrow_pattern, email_content)
            
            if tomorrow_match:
                hour = int(tomorrow_match.group(1))
                minute = int(tomorrow_match.group(2)) if tomorrow_match.group(2) else 0
                am_pm = tomorrow_match.group(3).lower() if tomorrow_match.group(3) else ""
                
                # Convert to 24-hour format
                if am_pm == "pm" and hour != 12:
                    hour += 12
                elif am_pm == "am" and hour == 12:
                    hour = 0
                
                # Calculate tomorrow's date
                tomorrow = base_date + timedelta(days=1)
                preferred_dt = tomorrow.replace(hour=hour, minute=minute, second=0)
                preferred_datetime = preferred_dt.strftime('%Y-%m-%dT%H:%M:%S+05:30')
            
            # Pattern: "6:00 AM IST" or similar
            time_pattern = r"(\d{1,2}):?(\d{0,2})\s*(am|pm|AM|PM)\s*(ist|IST)?"
            time_match = re.search(time_pattern, email_content)
            
            if time_match and not preferred_datetime:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2)) if time_match.group(2) else 0
                am_pm = time_match.group(3).lower() if time_match.group(3) else ""
                
                # Convert to 24-hour format
                if am_pm == "pm" and hour != 12:
                    hour += 12
                elif am_pm == "am" and hour == 12:
                    hour = 0
                
                # If "tomorrow" is mentioned, use tomorrow, otherwise use today or next day
                if "tomorrow" in email_lower:
                    target_date = base_date + timedelta(days=1)
                else:
                    target_date = base_date + timedelta(days=1)  # Default to next day
                
                preferred_dt = target_date.replace(hour=hour, minute=minute, second=0)
                preferred_datetime = preferred_dt.strftime('%Y-%m-%dT%H:%M:%S+05:30')
            
            # Fallback to default if no time found
            if not preferred_datetime:
                next_thursday = base_date + timedelta(days=(3 - base_date.weekday()) % 7)
                if next_thursday <= base_date:
                    next_thursday += timedelta(days=7)
                preferred_datetime = next_thursday.strftime('%Y-%m-%dT14:00:00+05:30')
            
            return {
                "duration_minutes": duration,
                "urgency": urgency,
                "preferred_datetime": preferred_datetime
            }
    
    def coordinate_scheduling(self, participants: List[str], meeting_info: Dict) -> Dict:
        """Coordinate between employee agents using A2A communication"""
        
        # Determine search window
        if meeting_info.get('preferred_datetime'):
            start_date = datetime.fromisoformat(meeting_info['preferred_datetime'].replace('+05:30', ''))
        else:
            start_date = datetime.now(self.ist_tz) + timedelta(days=1)
        
        search_days = {'urgent': 3, 'high': 7, 'medium': 14, 'low': 21}
        end_date = start_date + timedelta(days=search_days.get(meeting_info['urgency'], 14))
        
        start_str = start_date.strftime('%Y-%m-%dT00:00:00+05:30')
        end_str = end_date.strftime('%Y-%m-%dT23:59:59+05:30')
        
        # PHASE 0: Timezone Verification (NEW STEP)
        proposed_time = meeting_info.get('preferred_datetime', start_str)
        print(f"🔍 Timezone verification for proposed time: {proposed_time}")
        timezone_verification = self.timezone_agent.verify_timezone_compatibility(
            proposed_time, self.employee_agents
        )
        print(f"🔍 Timezone verification result: {json.dumps(timezone_verification, indent=2)}")
        
        # If timezone incompatible, use suggested alternative
        if not timezone_verification.get('compatible', True):
            suggested_time = timezone_verification.get('suggested_alternative', proposed_time)
            print(f"Timezone conflict detected. Using suggested time: {suggested_time}")
            meeting_info['preferred_datetime'] = suggested_time
            # Recalculate search window with new time
            start_date = datetime.fromisoformat(suggested_time.replace('+05:30', ''))
            start_str = start_date.strftime('%Y-%m-%dT00:00:00+05:30')
            end_str = (start_date + timedelta(days=search_days.get(meeting_info['urgency'], 14))).strftime('%Y-%m-%dT23:59:59+05:30')
        
        # Phase 1: Each employee agent finds their available slots
        all_proposals = {}
        for participant in participants:
            if participant in self.employee_agents:
                agent = self.employee_agents[participant]
                slots = agent.find_available_slots(start_str, end_str, meeting_info['duration_minutes'])
                all_proposals[participant] = slots
        
        # Phase 2: A2A negotiation between agents
        negotiation_results = []
        for participant in participants:
            if participant in self.employee_agents:
                agent = self.employee_agents[participant]
                other_proposals = [slots[:3] for email, slots in all_proposals.items() if email != participant]
                result = agent.negotiate_slot(all_proposals[participant], other_proposals)
                negotiation_results.append(result)
        
        # Phase 3: Boss agent makes final decision
        final_decision = self.make_final_decision(negotiation_results, meeting_info)
        
        # Add timezone verification info to final decision
        final_decision['timezone_verification'] = timezone_verification
        
        return final_decision
    
    def make_final_decision(self, negotiation_results: List[Dict], meeting_info: Dict) -> Dict:
        """Boss agent's final scheduling decision with fallback"""
        try:
            prompt = f"""Boss final decision.
Duration: {meeting_info['duration_minutes']}mins
Urgency: {meeting_info['urgency']}
Results: {json.dumps(negotiation_results[:3])}

Pick best time with highest consensus.
Return: {{"start":"2025-07-17T14:00:00+05:30","end":"2025-07-17T14:30:00+05:30","confidence":0.95}}"""
            
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
            # Fallback - pick from negotiation results or default
            if negotiation_results:
                best_result = max(negotiation_results, key=lambda x: x.get('confidence', 0))
                return {
                    "start": best_result["start"],
                    "end": best_result["end"],
                    "confidence": best_result.get("confidence", 0.7)
                }
            else:
                # Ultimate fallback
                preferred_dt = meeting_info.get('preferred_datetime', '2025-07-17T14:00:00+05:30')
                start_dt = datetime.fromisoformat(preferred_dt.replace('+05:30', ''))
                end_dt = start_dt + timedelta(minutes=meeting_info['duration_minutes'])
                return {
                    "start": start_dt.strftime('%Y-%m-%dT%H:%M:%S+05:30'),
                    "end": end_dt.strftime('%Y-%m-%dT%H:%M:%S+05:30'),
                    "confidence": 0.6
                }

def your_meeting_assistant(data):
    """Main function that processes meeting requests"""
    try:
        # Initialize Boss Agent
        boss = BossAgent()
        
        # Parse meeting request
        meeting_info = boss.parse_meeting_request(
            data['EmailContent'],
            data['Datetime']
        )
        
        # Get all participants
        all_participants = [data['From']] + [a['email'] for a in data['Attendees']]
        
        # Coordinate scheduling through agents
        scheduled_meeting = boss.coordinate_scheduling(all_participants, meeting_info)
        
        # Get all calendar events for output format
        search_date = datetime.fromisoformat(scheduled_meeting['start'].replace('+05:30', ''))
        day_start = search_date.strftime('%Y-%m-%dT00:00:00+05:30')
        day_end = search_date.strftime('%Y-%m-%dT23:59:59+05:30')
        
        # Build output format exactly as specified
        attendees_with_events = []
        for participant in all_participants:
            events = []
            
            # Get existing events if agent exists
            if participant in boss.employee_agents:
                events = boss.employee_agents[participant].get_calendar_events(day_start, day_end)
            
            # Add the new scheduled meeting
            events.append({
                "StartTime": scheduled_meeting['start'],
                "EndTime": scheduled_meeting['end'],
                "NumAttendees": len(all_participants),
                "Attendees": all_participants,
                "Summary": data.get('Subject', 'Meeting')
            })
            
            attendees_with_events.append({
                "email": participant,
                "events": events
            })
        
        # Create output in exact format
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
                "scheduling_step": "Boss Agent verified timezone compatibility before scheduling"
            }
        }
        
        # Create processed format
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

# Flask server
app = Flask(__name__)  
received_data = []

@app.route('/receive', methods=['POST'])
def receive():
    data = request.get_json()
    print(f"\nReceived: {json.dumps(data, indent=2)}")
    new_data = your_meeting_assistant(data)
    received_data.append(data)
    print(f"\n\n\nSending:\n {json.dumps(new_data, indent=2)}")
    return jsonify(new_data)

def run_flask():
    app.run(host='0.0.0.0', port=5001)

if __name__ == "__main__": 
    run_flask()