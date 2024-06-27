"""
reference: https://github.com/SocialSisterYi/bilibili-API-collect
"""


class LoginRequestState:
    Unknown = -1
    Pending = 86101  # 等待扫码
    Scanned = 86090  # 已扫码, 等待登录
    Expired = 86038  # 已过期
    Success = 0