class UserUtil:
    system_user = {
        "id": "74593ffb-07c0-ee54-79c1-98bf5d9fff83",
        "created_at": "2023-07-02 16:28:00.997962",
        "updated_at": "2023-07-02 16:28:00.997962",
        "created_user": "74593ffb-07c0-ee54-79c1-98bf5d9fff83",
        "updated_user": "74593ffb-07c0-ee54-79c1-98bf5d9fff83",
        "is_deleted": False,
        "email": "system@test.com",
        "last_name": "システム",
        "first_name": "ユーザー",
        "join_on": "2023-07-02",
        "retirement_on": None,
    }

    @classmethod
    def get_login_user(cls):
        """ログインユーザーを取得"""
        # TODO: いつかログインユーザーにする
        return cls.system_user
