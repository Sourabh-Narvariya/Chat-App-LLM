"""Create Flask app - simplified for beginners"""
from flask import Flask
from flask_cors import CORS
import config.config as config
from app.services.llm_service import LLMService
from app.services.chat_service import ChatService
from app.utils.memory_manager import MemoryManager
from app.utils.embeddings import EmbeddingManager

def create_app():
    """Create Flask app"""
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = "dev-secret-key"
    CORS(app)  # Allow frontend to call API
    
    # Setup services
    print("Setting up chat services...")
    
    llm = LLMService(config.GROQ_API_KEY, config.GROQ_MODEL)
    memory = MemoryManager(config.PINECONE_API_KEY, config.PINECONE_INDEX)
    embeddings = EmbeddingManager(config.EMBEDDING_MODEL)
    chat = ChatService(llm, memory, embeddings)
    
    app.chat_service = chat
    
    # Register routes
    from app.routes.chat import chat_bp
    from app.routes.web import web_bp
    
    app.register_blueprint(chat_bp)
    app.register_blueprint(web_bp)
    
    print("✓ App ready!")
    return app
