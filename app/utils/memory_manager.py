"""Memory storage using Pinecone"""
from pinecone import Pinecone
from datetime import datetime
import uuid

class MemoryManager:
    """Store and retrieve chat history"""
    
    def __init__(self, api_key, index_name):
        """Connect to Pinecone"""
        self.pc = Pinecone(api_key=api_key)
        self.index = self.pc.Index(index_name)
    
    def store_message(self, session_id, embedding, message, role):
        """Save message to database"""
        message_id = str(uuid.uuid4())
        
        # Save to Pinecone
        self.index.upsert(
            vectors=[(
                message_id,
                embedding,
                {
                    "session_id": session_id,
                    "message": message[:500],
                    "role": role,
                    "timestamp": datetime.now().isoformat()
                }
            )]
        )
        return message_id
    
    def retrieve_similar_messages(self, session_id, embedding, top_k=5):
        """Find similar past messages"""
        results = self.index.query(
            vector=embedding,
            top_k=top_k,
            filter={"session_id": {"$eq": session_id}},
            include_metadata=True
        )
        
        messages = []
        for match in results.get("matches", []):
            messages.append({
                "id": match["id"],
                "score": match["score"],
                "metadata": match["metadata"]
            })
        return messages
    
    def get_session_history(self, session_id, limit=10):
        """Get all messages from session"""
        dummy = [0.0] * 384  # Empty vector
        
        results = self.index.query(
            vector=dummy,
            top_k=limit,
            filter={"session_id": {"$eq": session_id}},
            include_metadata=True
        )
        
        messages = [match["metadata"] for match in results.get("matches", [])]
        return sorted(messages, key=lambda x: x.get("timestamp", ""))
    
    def delete_session_messages(self, session_id):
        """Delete all messages in session"""
        dummy = [0.0] * 384
        results = self.index.query(
            vector=dummy,
            top_k=1000,
            filter={"session_id": {"$eq": session_id}}
        )
        
        ids = [match["id"] for match in results.get("matches", [])]
        if ids:
            self.index.delete(ids=ids)
        return True
