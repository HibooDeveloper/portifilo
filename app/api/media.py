"""app/api/media.py — File upload & media manager"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app import db
from app.models import MediaFile
from app.utils.rbac import roles_required
import os, uuid, imghdr

media_bp = Blueprint('media', __name__)

ALLOWED = {'jpg','jpeg','png','webp','pdf'}
BLOCKED  = {'exe','bat','sh','php','js','rb','py'}

def _ext(fname): return fname.rsplit('.',1)[-1].lower() if '.' in fname else ''
def _allowed(fname): return _ext(fname) in ALLOWED and _ext(fname) not in BLOCKED

@media_bp.route('/', methods=['GET'])
@jwt_required()
@roles_required('admin','super_admin','editor')
def list_media():
    folder = request.args.get('folder')
    page   = int(request.args.get('page',1))
    q = MediaFile.query
    if folder: q = q.filter_by(folder=folder)
    pag = q.order_by(MediaFile.created_at.desc()).paginate(page=page, per_page=24, error_out=False)
    lang = request.args.get('lang','en')
    return jsonify({'items': [m.to_dict(lang) for m in pag.items], 'total': pag.total, 'pages': pag.pages}), 200

@media_bp.route('/upload', methods=['POST'])
@jwt_required()
@roles_required('admin','super_admin','editor')
def upload():
    if 'file' not in request.files: return jsonify({'error': 'No file'}), 400
    f = request.files['file']
    if not f.filename:               return jsonify({'error': 'Empty filename'}), 400
    if not _allowed(f.filename):     return jsonify({'error': 'File type not allowed'}), 400

    # Validate MIME for images
    ext   = _ext(f.filename)
    fname = f"{uuid.uuid4().hex}.{ext}"
    folder= request.form.get('folder','general')
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
    os.makedirs(upload_dir, exist_ok=True)
    fpath = os.path.join(upload_dir, fname)
    f.save(fpath)

    if ext in {'jpg','jpeg','png','webp'}:
        detected = imghdr.what(fpath)
        if detected not in {'jpeg','png','webp','gif'}:
            os.remove(fpath); return jsonify({'error': 'Invalid image file'}), 400

    size = os.path.getsize(fpath)
    if size > current_app.config['MAX_CONTENT_LENGTH']:
        os.remove(fpath); return jsonify({'error': 'File too large'}), 400

    url = f"/uploads/{folder}/{fname}"
    m   = MediaFile(filename=fname, original_name=secure_filename(f.filename),
                    file_path=fpath, url=url, mime_type=f.content_type,
                    file_size=size, folder=folder, uploaded_by=get_jwt_identity())
    db.session.add(m); db.session.commit()
    return jsonify(m.to_dict(request.args.get('lang','en'))), 201

@media_bp.route('/<int:mid>', methods=['DELETE'])
@jwt_required()
@roles_required('admin','super_admin')
def delete_media(mid):
    m = MediaFile.query.get_or_404(mid)
    try: os.remove(m.file_path)
    except FileNotFoundError: pass
    db.session.delete(m); db.session.commit()
    return jsonify({'message': 'Deleted'}), 200
