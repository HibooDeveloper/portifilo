"""app/api/analytics.py — Analytics tracking + dashboard"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
from sqlalchemy import func
from app import db, limiter
from app.models import AnalyticsEvent
from app.utils.rbac import roles_required
import json, hashlib

analytics_bp = Blueprint('analytics', __name__)

def _hash_ip(ip): return hashlib.sha256(ip.encode()).hexdigest()[:16]

@analytics_bp.route('/track', methods=['POST'])
@limiter.limit('300 per hour')
def track():
    d  = request.get_json(silent=True) or {}
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    ev = AnalyticsEvent(
        event_type=d.get('event_type','page_view')[:50],
        path=d.get('path','')[:512],
        referrer=d.get('referrer','')[:512],
        device=d.get('device','desktop')[:20],
        browser=d.get('browser','')[:50],
        lang=d.get('lang','en')[:5],
        ip_address=_hash_ip(ip),
        session_id=d.get('session_id','')[:64],
        meta=json.dumps(d.get('meta',{})) if d.get('meta') else None,
        user_agent=request.headers.get('User-Agent','')[:512],
    )
    db.session.add(ev); db.session.commit()
    return jsonify({'ok': True}), 201

@analytics_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@roles_required('admin','super_admin','viewer')
def dashboard():
    days   = int(request.args.get('days', 30))
    since  = datetime.utcnow() - timedelta(days=days)
    base   = AnalyticsEvent.query.filter(AnalyticsEvent.created_at >= since)

    total_views    = base.filter_by(event_type='page_view').count()
    unique_sessions= db.session.query(func.count(func.distinct(AnalyticsEvent.session_id))).filter(AnalyticsEvent.created_at >= since).scalar()
    top_pages      = db.session.query(AnalyticsEvent.path, func.count().label('c'))\
                       .filter(AnalyticsEvent.created_at >= since, AnalyticsEvent.event_type=='page_view')\
                       .group_by(AnalyticsEvent.path).order_by(func.count().desc()).limit(10).all()
    by_device      = db.session.query(AnalyticsEvent.device, func.count().label('c'))\
                       .filter(AnalyticsEvent.created_at >= since)\
                       .group_by(AnalyticsEvent.device).all()
    by_lang        = db.session.query(AnalyticsEvent.lang, func.count().label('c'))\
                       .filter(AnalyticsEvent.created_at >= since)\
                       .group_by(AnalyticsEvent.lang).all()
    daily          = db.session.query(func.date(AnalyticsEvent.created_at).label('day'), func.count().label('c'))\
                       .filter(AnalyticsEvent.created_at >= since, AnalyticsEvent.event_type=='page_view')\
                       .group_by(func.date(AnalyticsEvent.created_at)).order_by('day').all()

    return jsonify({
        'period_days': days,
        'total_views': total_views,
        'unique_sessions': unique_sessions,
        'top_pages':  [{'path': r[0], 'views': r[1]} for r in top_pages],
        'by_device':  [{'device': r[0], 'count': r[1]} for r in by_device],
        'by_lang':    [{'lang': r[0], 'count': r[1]} for r in by_lang],
        'daily':      [{'date': str(r[0]), 'views': r[1]} for r in daily],
    }), 200
