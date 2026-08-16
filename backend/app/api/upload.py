import uuid

from flask import Blueprint, request, current_app

from ..utils.response import success, error
from ..utils.auth import login_required
from ..utils.storage import save_file

upload_bp = Blueprint('upload', __name__, url_prefix='/api/upload')

ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024


def _allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route('', methods=['POST'])
@login_required
def upload_file():
    try:
        if 'file' not in request.files:
            return error('未选择文件')

        file = request.files['file']
        if not file.filename:
            return error('文件名为空')

        if not _allowed_file(file.filename):
            return error('仅支持 PDF 格式')

        file.seek(0, 2)
        size = file.tell()
        file.seek(0)

        if size > MAX_FILE_SIZE:
            return error(f'文件大小超过限制（最大 {MAX_FILE_SIZE // 1024 // 1024}MB）')

        ext = file.filename.rsplit('.', 1)[1].lower()
        safe_name = f"{uuid.uuid4().hex}.{ext}"

        save_file(file, safe_name)

        return success({
            'filename': safe_name,
            'originalName': file.filename,
            'size': size,
        }, msg='上传成功')
    except Exception as e:
        return error(str(e))
