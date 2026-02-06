"""
Chatbot Routes
NLP conversational interface for dietary advice
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.services.chatbot_service import ChatbotService

chatbot_bp = Blueprint('chatbot', __name__)
chatbot_service = ChatbotService()

@chatbot_bp.route('/')
@login_required
def chat():
    """Main chatbot interface"""
    # Get recent conversation history
    history = chatbot_service.get_conversation_history(current_user, limit=20)
    
    return render_template('chatbot/chat.html', history=history)

@chatbot_bp.route('/message', methods=['POST'])
@login_required
def send_message():
    """Send a message to the chatbot"""
    data = request.get_json()
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({'success': False, 'error': 'Message cannot be empty'}), 400
    
    # Process message
    response = chatbot_service.process_message(current_user, message)
    
    return jsonify({
        'success': True,
        'response': response['response'],
        'intent': response['intent'],
        'entities': response['entities']
    })

@chatbot_bp.route('/history')
@login_required
def get_history():
    """Get conversation history"""
    limit = request.args.get('limit', 20, type=int)
    history = chatbot_service.get_conversation_history(current_user, limit=limit)
    
    return jsonify({
        'success': True,
        'history': [h.to_dict() for h in history]
    })

