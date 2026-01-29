"""Chat service - handles conversations"""
import uuid

class ChatService:
    """Manages chat conversations"""
    
    def __init__(self, llm, memory, embeddings):
        self.llm = llm
        self.memory = memory
        self.embeddings = embeddings
    
    def create_session(self):
        """Create new chat session"""
        return str(uuid.uuid4())
    
    def chat(self, session_id, user_message, use_memory=True):
        """Send message and get AI response"""
        # 1. Get chat history
        history = self.memory.get_session_history(session_id) if use_memory else []
        
        # 2. Convert message to embedding
        user_embedding = self.embeddings.get_embedding(user_message)
        
        # 3. Find similar past messages
        context = []
        if use_memory:
            similar = self.memory.retrieve_similar_messages(session_id, user_embedding, top_k=5)
            context = [msg["metadata"].get("message", "") for msg in similar]
        
        # 4. Create prompt with context
        system_prompt = self.llm.generate_system_prompt(context)
        
        # 5. Format all messages
        messages = self.llm.format_messages(system_prompt, history, user_message)
        
        # 6. Get AI response
        response = self.llm.generate_response(messages)
        
        # 7. Save user message
        self.memory.store_message(session_id, user_embedding, user_message, "user")
        
        # 8. Save AI response
        response_embedding = self.embeddings.get_embedding(response)
        self.memory.store_message(session_id, response_embedding, response, "assistant")
        
        return response, {"session_id": session_id}
    
    def get_session_history(self, session_id):
        """Get all messages"""
        return self.memory.get_session_history(session_id)
    
    def clear_session(self, session_id):
        """Delete all messages"""
        self.memory.delete_session_messages(session_id)
        return True
