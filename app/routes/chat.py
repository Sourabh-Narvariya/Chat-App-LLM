"""API routes for chat"""
from flask import Blueprint, request, jsonify, current_app

chat_bp = Blueprint("chat", __name__, url_prefix="/api/chat")

@chat_bp.route("/session", methods=["POST"])
def create_session():
    """Create new chat session"""
    session_id = current_app.chat_service.create_session()
    return jsonify({"session_id": session_id}), 201

@chat_bp.route("/message", methods=["POST"])
def send_message():
    """Send message and get response"""
    data = request.get_json()
    
    if not data or "session_id" not in data or "message" not in data:
        return jsonify({"error": "Missing session_id or message"}), 400
    
    session_id = data["session_id"]
    user_message = data["message"]
    use_memory = data.get("use_memory", True)
    
    response, metadata = current_app.chat_service.chat(
        session_id, user_message, use_memory=use_memory
    )
    
    return jsonify({"response": response, "metadata": metadata}), 200

@chat_bp.route("/history/<session_id>", methods=["GET"])
def get_history(session_id):
    """Get chat history"""
    history = current_app.chat_service.get_session_history(session_id)
    return jsonify({"history": history}), 200

@chat_bp.route("/clear/<session_id>", methods=["DELETE"])
def clear_session(session_id):
    """Clear chat history"""
    current_app.chat_service.clear_session(session_id)
    return jsonify({"message": "Session cleared"}), 200

@chat_bp.route("/health", methods=["GET"])
def health():
    """Health check"""
    return jsonify({"status": "healthy"}), 200
