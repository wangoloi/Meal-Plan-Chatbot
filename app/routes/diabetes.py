"""
Diabetes Management Routes
Handles Type 1 and Type 2 diabetes support
"""
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import DiabetesRecord, User
from datetime import datetime
import json

diabetes_bp = Blueprint('diabetes', __name__)

@diabetes_bp.route('/dashboard')
@login_required
def dashboard():
    """Diabetes management dashboard"""
    if not current_user.has_diabetes:
        flash('Diabetes features are only available for users with diabetes', 'info')
        return redirect(url_for('main.dashboard'))
    
    # Get recent records
    recent_records = DiabetesRecord.query.filter_by(
        user_id=current_user.id
    ).order_by(DiabetesRecord.created_at.desc()).limit(30).all()
    
    # Calculate statistics
    stats = _calculate_diabetes_stats(current_user)
    
    return render_template('diabetes/dashboard.html',
                         records=recent_records,
                         stats=stats,
                         user=current_user)

@diabetes_bp.route('/record', methods=['GET', 'POST'])
@login_required
def record_entry():
    """Record diabetes data (blood glucose, insulin, etc.)"""
    if not current_user.has_diabetes:
        return jsonify({'success': False, 'error': 'Not authorized'}), 403
    
    if request.method == 'POST':
        record_type = request.form.get('record_type') or request.json.get('record_type')
        
        record = DiabetesRecord(
            user_id=current_user.id,
            record_type=record_type
        )
        
        if record_type == 'blood_glucose':
            record.blood_glucose_level = float(request.form.get('blood_glucose_level') or request.json.get('blood_glucose_level', 0))
            record.measurement_time = datetime.fromisoformat(
                request.form.get('measurement_time') or request.json.get('measurement_time', datetime.utcnow().isoformat())
            )
            record.measurement_type = request.form.get('measurement_type') or request.json.get('measurement_type', 'random')
        
        elif record_type == 'insulin' and current_user.diabetes_type == 'type1':
            record.insulin_type = request.form.get('insulin_type') or request.json.get('insulin_type')
            record.insulin_units = float(request.form.get('insulin_units') or request.json.get('insulin_units', 0))
            record.insulin_time = datetime.fromisoformat(
                request.form.get('insulin_time') or request.json.get('insulin_time', datetime.utcnow().isoformat())
            )
            # For Type 1, connect to external system
            record.external_system_id = _sync_with_external_system(current_user, record)
        
        elif record_type == 'hba1c':
            record.hba1c_value = float(request.form.get('hba1c_value') or request.json.get('hba1c_value', 0))
            record.hba1c_date = datetime.fromisoformat(
                request.form.get('hba1c_date') or request.json.get('hba1c_date', datetime.utcnow().isoformat())
            )
        
        elif record_type == 'medication' and current_user.diabetes_type == 'type2':
            record.medication_name = request.form.get('medication_name') or request.json.get('medication_name')
            record.medication_dose = request.form.get('medication_dose') or request.json.get('medication_dose')
        
        record.notes = request.form.get('notes') or request.json.get('notes', '')
        
        db.session.add(record)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'record': record.to_dict()})
        
        flash('Record saved successfully', 'success')
        return redirect(url_for('diabetes.dashboard'))
    
    return render_template('diabetes/record.html', user=current_user)

@diabetes_bp.route('/insulin-recommendation', methods=['POST'])
@login_required
def insulin_recommendation():
    """Get insulin recommendation for Type 1 diabetes"""
    if current_user.diabetes_type != 'type1':
        return jsonify({'success': False, 'error': 'Only for Type 1 diabetes'}), 400
    
    data = request.get_json()
    blood_glucose = data.get('blood_glucose_level')
    carbs = data.get('carbohydrates', 0)
    
    # Get recommendation from external system
    recommendation = _get_insulin_recommendation(current_user, blood_glucose, carbs)
    
    return jsonify({
        'success': True,
        'recommendation': recommendation
    })

@diabetes_bp.route('/progress')
@login_required
def progress():
    """View diabetes progress and improvements"""
    if not current_user.has_diabetes:
        return redirect(url_for('main.dashboard'))
    
    # Get records for analysis
    records = DiabetesRecord.query.filter_by(
        user_id=current_user.id
    ).order_by(DiabetesRecord.created_at.asc()).all()
    
    # Analyze progress
    progress_data = _analyze_progress(records, current_user.diabetes_type)
    
    return render_template('diabetes/progress.html',
                         progress_data=progress_data,
                         user=current_user)

@diabetes_bp.route('/api/stats')
@login_required
def api_stats():
    """API endpoint for diabetes statistics"""
    if not current_user.has_diabetes:
        return jsonify({'success': False, 'error': 'Not authorized'}), 403
    
    stats = _calculate_diabetes_stats(current_user)
    return jsonify({'success': True, 'stats': stats})

def _calculate_diabetes_stats(user):
    """Calculate diabetes statistics"""
    records = DiabetesRecord.query.filter_by(
        user_id=user.id,
        record_type='blood_glucose'
    ).order_by(DiabetesRecord.created_at.desc()).limit(30).all()
    
    if not records:
        return {
            'avg_glucose': None,
            'glucose_range': None,
            'in_range_percentage': None,
            'trend': 'insufficient_data'
        }
    
    glucose_levels = [r.blood_glucose_level for r in records if r.blood_glucose_level]
    
    if not glucose_levels:
        return {'avg_glucose': None, 'glucose_range': None}
    
    avg_glucose = sum(glucose_levels) / len(glucose_levels)
    min_glucose = min(glucose_levels)
    max_glucose = max(glucose_levels)
    
    # Count in-range readings (70-180 mg/dL)
    in_range = sum(1 for g in glucose_levels if 70 <= g <= 180)
    in_range_percentage = (in_range / len(glucose_levels)) * 100
    
    # Determine trend
    if len(glucose_levels) >= 7:
        recent_avg = sum(glucose_levels[:7]) / 7
        older_avg = sum(glucose_levels[7:14]) / 7 if len(glucose_levels) >= 14 else avg_glucose
        if recent_avg < older_avg * 0.95:
            trend = 'improving'
        elif recent_avg > older_avg * 1.05:
            trend = 'worsening'
        else:
            trend = 'stable'
    else:
        trend = 'insufficient_data'
    
    return {
        'avg_glucose': round(avg_glucose, 1),
        'min_glucose': round(min_glucose, 1),
        'max_glucose': round(max_glucose, 1),
        'glucose_range': f"{min_glucose:.0f}-{max_glucose:.0f}",
        'in_range_percentage': round(in_range_percentage, 1),
        'total_readings': len(glucose_levels),
        'trend': trend
    }

def _sync_with_external_system(user, record):
    """Sync insulin data with external medical system"""
    # In production, this would make API calls to external system
    # For now, return a mock ID
    import uuid
    return f"ext_{uuid.uuid4().hex[:8]}"

def _get_insulin_recommendation(user, blood_glucose, carbs):
    """Get insulin recommendation from external system"""
    # In production, this would call external API
    # For now, provide basic calculation (NOT medical advice)
    
    recommendation = {
        'blood_glucose': blood_glucose,
        'carbohydrates': carbs,
        'warning': 'This is a demonstration. Consult your healthcare provider for actual insulin dosing.'
    }
    
    # Basic insulin calculation (simplified, NOT for actual use)
    if blood_glucose > 180:
        correction_insulin = (blood_glucose - 150) / 50  # Simplified correction factor
    else:
        correction_insulin = 0
    
    carb_insulin = carbs / 15  # Simplified carb ratio (1 unit per 15g carbs)
    
    recommendation['correction_units'] = round(correction_insulin, 1)
    recommendation['carb_units'] = round(carb_insulin, 1)
    recommendation['total_units'] = round(correction_insulin + carb_insulin, 1)
    
    return recommendation

def _analyze_progress(records, diabetes_type):
    """Analyze diabetes progress over time"""
    progress_data = {
        'glucose_trends': [],
        'hba1c_trends': [],
        'improvements': [],
        'concerns': []
    }
    
    # Analyze glucose trends
    glucose_records = [r for r in records if r.record_type == 'blood_glucose' and r.blood_glucose_level]
    if len(glucose_records) >= 7:
        recent_avg = sum(r.blood_glucose_level for r in glucose_records[:7]) / 7
        older_avg = sum(r.blood_glucose_level for r in glucose_records[7:14]) / 7 if len(glucose_records) >= 14 else recent_avg
        
        if recent_avg < older_avg:
            progress_data['improvements'].append(f"Average blood glucose improved from {older_avg:.1f} to {recent_avg:.1f} mg/dL")
        elif recent_avg > older_avg:
            progress_data['concerns'].append(f"Average blood glucose increased from {older_avg:.1f} to {recent_avg:.1f} mg/dL")
    
    # Analyze HbA1c trends
    hba1c_records = [r for r in records if r.record_type == 'hba1c' and r.hba1c_value]
    if len(hba1c_records) >= 2:
        latest = hba1c_records[0].hba1c_value
        previous = hba1c_records[1].hba1c_value
        
        if latest < previous:
            progress_data['improvements'].append(f"HbA1c improved from {previous:.1f}% to {latest:.1f}%")
        elif latest > previous:
            progress_data['concerns'].append(f"HbA1c increased from {previous:.1f}% to {latest:.1f}%")
    
    return progress_data

