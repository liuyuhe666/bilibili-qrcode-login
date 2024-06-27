from uuid import uuid4
import logging
from typing import Optional

import peewee
from flask import request
import requests

from modules import common
from modules.types import LoginRequestState
from modules.database import LoginRequest


def create_login_request() -> tuple[dict, int]:
    """创建登录请求"""
    uuid = str(uuid4())

    try:
        r = requests.get(
            url='https://passport.bilibili.com/x/passport-login/web/qrcode/generate',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
            }                 
        )
        data = r.json()['data']
        url = data['url']
        qrcode_key = data['qrcode_key']
    except (requests.RequestException, KeyError) as e:
        logging.error(f'创建登录请求失败: {e}')
        return {'code': 507, 'message': '创建登录请求失败.'}, 500

    try:
        login_request = LoginRequest.create(
            uuid=uuid,
            url=url,
            qrcode_key=qrcode_key,
            created_at=common.now(),
        )
    except peewee.PeeweeException as e:
        logging.error(f'创建登录请求失败: {e}')
        return {'code': 507, 'message': '创建登录请求失败.'}, 500

    return {
        'code': 200,
        'data': {
            'uuid': login_request.uuid,
            'url': url,
            'qrcode_key': qrcode_key,
            'state': login_request.state,
            'created_at': login_request.created_at,
        }
    }, 200


def query_login_request(login_request: LoginRequest) -> Optional[dict]:
    """
    查询登录请求

    :param login_request:
    :return:
    """
    r = requests.get(
        url=f'https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={login_request.qrcode_key}',
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
        }
    )

    data = r.json()['data']

    old_state = login_request.state
    new_state = LoginRequestState.Unknown

    if data['code'] == 86101:
        new_state = LoginRequestState.Pending
    elif data['code'] == 86090:
        new_state = LoginRequestState.Scanned
    elif data['code'] == 86038:
        new_state = LoginRequestState.Expired
    elif data['code'] == 0:
        new_state = LoginRequestState.Success

    if new_state != old_state:
        login_request.state = new_state
        login_request.save()

    user_data = {}
    if new_state == LoginRequestState.Success:
        cookie_dict = requests.utils.dict_from_cookiejar(r.cookies)
        user_data['DedeUserID'] = cookie_dict['DedeUserID']
        user_data['DedeUserID__ckMd5'] = cookie_dict['DedeUserID__ckMd5']
        user_data['SESSDATA'] = cookie_dict['SESSDATA']
        user_data['bili_jct'] = cookie_dict['bili_jct']
    
    return user_data or None


def get_login_request() -> tuple[dict, int]:
    """查询登录结果"""
    try:
        uuid = request.args['uuid']
    except (TypeError, KeyError, ValueError):
        return {'code': 400, 'message': '参数错误.'}, 400

    try:
        login_request = LoginRequest.get(LoginRequest.uuid == uuid)
    except peewee.DoesNotExist:
        return {'code': 404, 'message': '登录请求不存在.'}, 404
    except peewee.PeeweeException as e:
        logging.error(f'查询登录请求失败: {e}')
        return {'code': 507, 'message': '查询登录请求失败.'}, 500

    if common.now() > login_request.created_at + 1000 * 60 * 5:
        login_request.state = LoginRequestState.Expired
        login_request.save()

    user = None

    if login_request.state in (
        LoginRequestState.Pending,
        LoginRequestState.Scanned,
    ):
        try:
            user = query_login_request(login_request)
        except requests.exceptions.RequestException as e:
            logging.error(f'查询登录请求失败: {e}')
            return {'code': 507, 'message': '查询登录请求失败.'}, 500

    return {
        'code': 200,
        'data': {
            'uuid': login_request.uuid,
            'url': login_request.url,
            'qrcode_key': login_request.qrcode_key,
            'state': login_request.state,
            'created_at': login_request.created_at,
            'user': user,
        }
    }, 200