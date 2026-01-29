"""Talk to Groq AI"""
from groq import Groq

class LLMService:
    """Chat with Groq AI"""
    
    def __init__(self, api_key, model="mixtral-8x7b-32768"):
        """Setup Groq"""
        self.client = Groq(api_key=api_key)
        self.model = model
    
    def generate_response(self, messages):
        """Get AI response"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content
    
    def generate_system_prompt(self, context):
        """Create prompt with memory"""
        context_text = "\n".join(context) if context else "No previous context."
        return f"""You are a helpful AI assistant.

Previous conversation:
{context_text}

Be helpful and friendly."""
    
    def format_messages(self, system_prompt, history, user_message):
        """Format messages for AI"""
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add recent history
        for msg in history[-10:]:
            messages.append({"role": msg["role"], "content": msg["message"]})
        
        # Add user message
        messages.append({"role": "user", "content": user_message})
        return messages
