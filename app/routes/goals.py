"""
Goals and Progress Tracking Routes
"""
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Goal, GoalProgress
from datetime import datetime, timedelta

goals_bp = Blueprint('goals', __name__)

@goals_bp.route('/')
@login_required
def list_goals():
    """List all user goals"""
    status = request.args.get('status', 'active')
    
    goals = Goal.query.filter_by(
        user_id=current_user.id,
        status=status
    ).order_by(Goal.created_at.desc()).all()
    
    return render_template('goals/list.html', goals=goals, status=status)

@goals_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_goal():
    """Create a new goal"""
    if request.method == 'POST':
        goal_type = request.form.get('goal_type')
        target_value = float(request.form.get('target_value', 0))
        current_value = float(request.form.get('current_value', 0))
        unit = request.form.get('unit', 'kg')
        target_date_str = request.form.get('target_date')
        
        target_date = None
        if target_date_str:
            target_date = datetime.fromisoformat(target_date_str)
        
        goal = Goal(
            user_id=current_user.id,
            goal_type=goal_type,
            target_value=target_value,
            current_value=current_value,
            unit=unit,
            target_date=target_date,
            status='active'
        )
        
        db.session.add(goal)
        db.session.commit()
        
        flash('Goal created successfully!', 'success')
        return redirect(url_for('goals.view_goal', goal_id=goal.id))
    
    return render_template('goals/create.html')

@goals_bp.route('/<int:goal_id>')
@login_required
def view_goal(goal_id):
    """View a specific goal and its progress"""
    goal = Goal.query.get_or_404(goal_id)
    
    if goal.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('goals.list_goals'))
    
    # Get progress updates
    progress_updates = GoalProgress.query.filter_by(
        goal_id=goal_id
    ).order_by(GoalProgress.created_at.desc()).all()
    
    return render_template('goals/view.html',
                         goal=goal,
                         progress_updates=progress_updates)

@goals_bp.route('/<int:goal_id>/update', methods=['POST'])
@login_required
def update_goal(goal_id):
    """Update goal progress"""
    goal = Goal.query.get_or_404(goal_id)
    
    if goal.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    data = request.get_json() or request.form
    new_value = float(data.get('value', 0))
    notes = data.get('notes', '')
    
    # Update current value
    goal.current_value = new_value
    goal.updated_at = datetime.utcnow()
    
    # Check if goal is completed
    if goal.goal_type == 'lose_weight' and new_value <= goal.target_value:
        goal.status = 'completed'
    elif goal.goal_type == 'gain_weight' and new_value >= goal.target_value:
        goal.status = 'completed'
    elif goal.goal_type == 'maintain_weight':
        # Within 2% of target
        if abs(new_value - goal.target_value) / goal.target_value < 0.02:
            goal.status = 'completed'
    
    # Record progress
    progress = GoalProgress(
        goal_id=goal_id,
        value=new_value,
        notes=notes
    )
    db.session.add(progress)
    db.session.commit()
    
    if request.is_json:
        return jsonify({
            'success': True,
            'goal': goal.to_dict(),
            'progress': progress.value
        })
    
    flash('Progress updated!', 'success')
    return redirect(url_for('goals.view_goal', goal_id=goal_id))

@goals_bp.route('/<int:goal_id>/complete', methods=['POST'])
@login_required
def complete_goal(goal_id):
    """Mark goal as completed"""
    goal = Goal.query.get_or_404(goal_id)
    
    if goal.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    goal.status = 'completed'
    db.session.commit()
    
    return jsonify({'success': True, 'goal': goal.to_dict()})

@goals_bp.route('/api/metrics')
@login_required
def api_metrics():
    """Get user metrics and statistics"""
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    
    active_goals = [g for g in goals if g.status == 'active']
    completed_goals = [g for g in goals if g.status == 'completed']
    
    metrics = {
        'total_goals': len(goals),
        'active_goals': len(active_goals),
        'completed_goals': len(completed_goals),
        'completion_rate': (len(completed_goals) / len(goals) * 100) if goals else 0,
        'goals': [g.to_dict() for g in goals]
    }
    
    return jsonify({'success': True, 'metrics': metrics})

