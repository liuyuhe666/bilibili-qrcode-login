# Bilibili QR Code Login

Obtain a `SESSDATA` by logging in through QR code scanning.

# 哔哩哔哩二维码登录

通过扫码登陆获取哔哩哔哩的 `SESSDATA`.

## Feature | 特性

- Out of the box | 开箱即用
- No privacy risk | 无隐私风险
- No extra service required | 不需要额外服务

## Important | 重要

SESSDATA will never be saved or uploaded to any server.

Only required parameters for log in will be saved in `database.db`.

And it can not be used to log in again or get any personal information.

You can find more details in `modules/login.py`.

SESSDATA 永远不会被保存或上传到任何服务器.

只有登陆所需的参数会被保存在 `database.db` 中.

并且它不能用于再次登陆或获取任何个人信息.

你可以在 `modules/login.py` 中找到更多细节.

## Self-hosted | 自托管

1. Install dependencies | 安装依赖

    ```bash
    pip install -r requirements.txt
    ```

2. Run | 运行

    ```bash
    python app.py
    ```

## Reference | 参考资料
- [https://github.com/SocialSisterYi/bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)
- [https://github.com/ImYrS/aliyundrive-qr-login](https://github.com/ImYrS/aliyundrive-qr-login)