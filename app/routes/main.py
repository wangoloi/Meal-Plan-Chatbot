from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@main_bp.route('/onboarding', methods=['GET', 'POST'])
@login_required
def onboarding():
    """User onboarding to capture initial information"""
    if request.method == 'POST':
        # Update user profile
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        current_user.age = int(request.form.get('age', 0))
        current_user.gender = request.form.get('gender')
        current_user.height = float(request.form.get('height', 0))
        current_user.weight = float(request.form.get('weight', 0))
        current_user.activity_level = request.form.get('activity_level')
        
        # Health conditions
        has_diabetes = request.form.get('has_diabetes') == 'yes'
        current_user.has_diabetes = has_diabetes
        if has_diabetes:
            current_user.diabetes_type = request.form.get('diabetes_type')
        
        # Primary goal
        current_user.primary_goal = request.form.get('primary_goal')
        
        # Budget
        current_user.budget_range = request.form.get('budget_range')
        monthly_budget = request.form.get('monthly_budget')
        if monthly_budget:
            current_user.monthly_budget = float(monthly_budget)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('onboarding.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    user_data = current_user.to_dict()
    
    # Get recent recommendations
    from app.models import Recommendation
    recent_recommendations = Recommendation.query.filter_by(
        user_id=current_user.id
    ).order_by(Recommendation.created_at.desc()).limit(5).all()
    
    # Get active goals
    from app.models import Goal
    active_goals = Goal.query.filter_by(
        user_id=current_user.id,
        status='active'
    ).all()
    
    # Get recent diabetes records if applicable
    diabetes_records = []
    if current_user.has_diabetes:
        from app.models import DiabetesRecord
        diabetes_records = DiabetesRecord.query.filter_by(
            user_id=current_user.id
        ).order_by(DiabetesRecord.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html',
                         user=user_data,
                         recommendations=recent_recommendations,
                         goals=active_goals,
                         diabetes_records=diabetes_records)

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management"""
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        current_user.age = int(request.form.get('age', 0))
        current_user.height = float(request.form.get('height', 0))
        current_user.weight = float(request.form.get('weight', 0))
        current_user.activity_level = request.form.get('activity_level')
        current_user.budget_range = request.form.get('budget_range')
        
        monthly_budget = request.form.get('monthly_budget')
        if monthly_budget:
            current_user.monthly_budget = float(monthly_budget)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('profile.html', user=current_user)

