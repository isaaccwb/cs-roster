from flask import jsonify


def success(data=None, msg='操作成功'):
    return jsonify({'code': 0, 'msg': msg, 'data': data})


def error(msg='操作失败', code=-1):
    return jsonify({'code': code, 'msg': msg, 'data': None})
