import os
from flask import current_app

try:
    import boto3
    _BOTO3_AVAILABLE = True
except ImportError:
    _BOTO3_AVAILABLE = False


def _use_s3() -> bool:
    return bool(current_app.config.get('S3_BUCKET'))


def save_file(file_obj, filename: str) -> str:
    """保存文件，返回访问路径。
    线上（配置了 S3_BUCKET）→ 上传到 S3，返回 S3 URL。
    本地（未配置 S3_BUCKET）→ 保存到本地 uploads 目录，返回相对路径。
    """
    if _use_s3():
        bucket = current_app.config['S3_BUCKET']
        region = current_app.config['AWS_REGION']
        client = boto3.client('s3', region_name=region)
        client.upload_fileobj(file_obj, bucket, filename)
        return f"https://{bucket}.s3.{region}.amazonaws.com/{filename}"

    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)
    file_obj.save(filepath)
    return f"/uploads/{filename}"


def delete_file(filename: str) -> None:
    """删除文件。"""
    if _use_s3():
        bucket = current_app.config['S3_BUCKET']
        region = current_app.config['AWS_REGION']
        client = boto3.client('s3', region_name=region)
        client.delete_object(Bucket=bucket, Key=filename)
        return

    upload_folder = current_app.config['UPLOAD_FOLDER']
    filepath = os.path.join(upload_folder, filename)
    if os.path.exists(filepath):
        os.remove(filepath)


def get_file_url(filename: str) -> str:
    """获取文件访问 URL。"""
    if _use_s3():
        bucket = current_app.config['S3_BUCKET']
        region = current_app.config['AWS_REGION']
        return f"https://{bucket}.s3.{region}.amazonaws.com/{filename}"

    return f"/uploads/{filename}"
