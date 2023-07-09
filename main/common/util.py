from django.utils import timezone


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


class Bulk:
    """バルク処理の共通クラス"""
    UPDATED_USER_FIELD = "updated_user_id"
    CREATED_USER_FIELD = "created_user_id"
    UPDATED_AT = "updated_at"
    CREATED_AT = "created_at"

    @classmethod
    def update(cls, model, data_qs, fields):
        """一括更新"""
        now = timezone.now()
        # NOTE: bulk時は、saveメソッドを通らないため、値を指定する
        login_user = UserUtil.get_login_user()
        for data in data_qs:
            data.updated_user_id = login_user["id"]
            data.updated_at = now

        # フィールド追加
        if cls.UPDATED_USER_FIELD not in fields:
            fields.append(cls.UPDATED_USER_FIELD)
        if cls.UPDATED_AT not in fields:
            fields.append(cls.UPDATED_AT)

        model.objects.bulk_update(data_qs, fields=fields)

    @classmethod
    def created(cls, model, data_qs):
        """一括作成"""
        now = timezone.now()
        # NOTE: bulk時は、saveメソッドを通らないため、値を指定する
        login_user = UserUtil.get_login_user()
        for data in data_qs:
            data.updated_user_id = login_user["id"]
            data.created_user_id = login_user["id"]
            data.updated_at = now
            data.created_at = now

        model.objects.bulk_update(data_qs)
