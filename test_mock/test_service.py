# test_service.py
import pytest
import sys
from unittest.mock import MagicMock

# 关键点：在导入 service 前，动态创建模拟的 database 模块
sys.modules["database"] = MagicMock()  # 避免 ModuleNotFoundError
# sys.modules["database"] = MagicMock() 不是动态导入，而是一种 动态模块替换 技术。它的作用是 在运行时替换或创建模块，而不是直接导入模块。

from service import UserService  # 现在可以安全导入了


class TestUserService:
    @pytest.fixture
    def mock_db(self, mocker):
        """模拟 database.connect 和查询结果"""
        # 获取模拟的 database 模块
        mock_database_module = sys.modules["database"]

        # 创建模拟的数据库连接对象
        mock_conn = mocker.MagicMock()
        # 让 database.connect() 返回这个模拟连接
        mocker.patch.object(mock_database_module, "connect", return_value=mock_conn)

        return mock_conn  # 返回模拟连接，用于后续操作（如设置 query 返回值）

    @pytest.fixture
    def mock_requests(self, mocker):
        """模拟 requests.get"""
        return mocker.patch("requests.get")

    def test_get_user_profile_success(self, mock_db, mock_requests):
        # 设置数据库查询返回模拟用户
        mock_user = MagicMock()
        mock_user.id = 123
        mock_user.name = "Alice"
        mock_user.email = "alice@example.com"
        mock_db.query.return_value = mock_user  # 关键：设置 query 方法返回值

        # 设置 API 返回
        mock_response = mock_requests.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"age": 30, "country": "US"}

        # 调用被测方法
        service = UserService()
        result = service.get_user_profile(123)

        # 验证结果
        assert result == {
            "id": 123,
            "name": "Alice",
            "email": "alice@example.com",
            "api_data": {"age": 30, "country": "US"}
        }

        # 验证数据库和 API 调用行为
        mock_db.query.assert_called_once_with("SELECT * FROM users WHERE id = ?", 123)
        mock_requests.assert_called_once_with("https://api.example.com/profile/123")

    # 其他测试用例保持不变...
    def test_user_not_found(self, mock_db):
        """测试用户不存在的情况"""
        mock_db.query.return_value = None  # 模拟数据库无结果

        service = UserService()
        with pytest.raises(ValueError, match="用户不存在"):
            service.get_user_profile(456)

    def test_api_failure(self, mock_db, mock_requests):
        """测试API请求失败"""
        mock_user = mock_db.query.return_value
        mock_user.id = 789

        mock_response = mock_requests.return_value
        mock_response.status_code = 500  # 模拟API返回错误

        service = UserService()
        with pytest.raises(ConnectionError, match="API请求失败"):
            service.get_user_profile(789)