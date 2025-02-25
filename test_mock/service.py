# service.py
import requests
import database


class UserService:
    def get_user_profile(self, user_id):
        """获取用户资料（依赖数据库和外部API）"""
        # 数据库操作
        conn = database.connect()
        user = conn.query("SELECT * FROM users WHERE id = ?", user_id)
        if not user:
            raise ValueError("用户不存在")

        # 调用外部API
        api_url = f"https://api.example.com/profile/{user.id}"
        response = requests.get(api_url)
        if response.status_code != 200:
            raise ConnectionError("API请求失败")

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "api_data": response.json()
        }