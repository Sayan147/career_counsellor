from typing import List
import google.generativeai as genai
from ..core.config import get_settings
from ..db.csv_storage import create_chat, get_user_chats, get_user_profile
from datetime import datetime
from ..models.messages import SystemMessage, HumanMessage, AIMessage

settings = get_settings()

class CareerCounselor:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.base_system_message = """You are an experienced career counselor with deep knowledge of academic programs, job roles,
              industry trends, and skill requirements across various domains. Your goal is to guide students in 
              making informed decisions about their education and career paths based on their interests, academic background, 
              and skills. Always be supportive, realistic, and provide actionable suggestions. 
              Use simple language, short, crisp and to the point answers with maximum 1 or 2 examples relevant to students in college or about to graduate. 
              Recommend career options, relevant certifications, higher studies, or job roles depending on the user input. 
              Provide the answer which can be real and practical according to the user's condition, situations and question."""

    def get_chat_response(self, message: str, user: dict, system_message: SystemMessage = None) -> str:
        # Get AI response
        response = self._generate_response(message, user, system_message)
        
        # Save chat to CSV
        create_chat(user["id"], message, response)
        
        return response

    def _generate_response(self, message: str, user: dict, system_message: SystemMessage = None) -> str:
        try:
            # Get user profile
            profile = get_user_profile(user["id"])
            
            # Create system message with profile context if available
            system_content = self.base_system_message
            if profile:
                profile_context = f"""
                Consider the following information about the user:
                - Name: {profile['full_name']}
                - Age: {profile['age']}
                - Skills: {', '.join(profile['skills'])}
                - Experience: {profile['experience']}
                - Education:
                """
                for edu in profile['education']:
                    profile_context += f"\n  * {edu['level']} from {edu['institution']} with score {edu['score']} ({edu['year_completed']})"
                
                system_content = f"{system_content}\n\n{profile_context}"
            
            # Use provided system message or create default one
            system_msg = system_message or SystemMessage(content=system_content)
            
            # Create human message
            human_msg = HumanMessage(content=message)
            
            # Combine messages into prompt
            prompt = f"{system_msg.role}: {system_msg.content}\n{human_msg.role}: {human_msg.content}"
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"

    def get_chat_history(self, user: dict) -> List[dict]:
        # Get chat history from CSV
        chats = get_user_chats(user["id"])
        
        return [
            {
                "message": chat["message"],
                "response": chat["response"],
                "timestamp": chat["created_at"]
            }
            for chat in chats
        ] 