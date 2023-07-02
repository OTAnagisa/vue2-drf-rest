import uuid
from datetime import datetime

from django.db import models
from django.db.models import Q
from sequences import get_next_value

from main.common.util import UserUtil


class User(models.Model):
    """ユーザー"""

    # id
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 作成日時
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新日時
    updated_at = models.DateTimeField(auto_now=True)
    # 作成者
    created_user = models.ForeignKey("self", on_delete=models.CASCADE, related_name="+")
    # 更新者
    updated_user = models.ForeignKey("self", on_delete=models.CASCADE, related_name="+")
    # 削除フラグ
    is_deleted = models.BooleanField(default=False)
    # メールアドレス
    email = models.EmailField()
    # 苗字
    last_name = models.CharField(max_length=25)
    # 氏名
    first_name = models.CharField(max_length=25)
    # 入社日
    join_on = models.DateField(null=True)
    # 退職日
    retirement_on = models.DateField(null=True)

    objects = models.Manager()

    def full_name(self):
        """フルネーム取得用"""
        return f"{self.last_name}　{self.first_name}"

    class Meta:
        db_table = "user"


class BaseModel(models.Model):
    """ベースモデル"""

    # id
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 作成日時
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新日時
    updated_at = models.DateTimeField(auto_now=True)
    # 作成者
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    # 更新者
    updated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    # 削除フラグ
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        """saveメソッドをオーバーライド"""
        # ログインユーザーを登録
        login_user = UserUtil.get_login_user
        self.created_user = self.created_user or login_user
        self.updated_user = login_user
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id

    class Meta:
        # 抽象基底クラス定義
        abstract = True


class NewsCategory(BaseModel):
    """お知らせカテゴリー"""

    # カテゴリー名
    name = models.CharField(max_length=30)
    # 表示順
    order = models.IntegerField()
    # コード値
    code = models.IntegerField()

    class Meta:
        db_table = "news_category"


class News(BaseModel):
    """お知らせ"""

    # タイトル
    title = models.CharField(max_length=30)
    # 本文
    contents = models.TextField()
    # 掲載日
    publication_on = models.DateField(null=True)
    # お知らせNo
    no = models.IntegerField(unique=True)
    # カテゴリー
    category = models.ForeignKey(NewsCategory, on_delete=models.PROTECT)
    # 作成者
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.no:
            self.no = get_next_value("news_no")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "news"


class Department(BaseModel):
    """部"""

    # 部名
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "department"


class Section(BaseModel):
    """課"""

    # 課名
    name = models.CharField(max_length=100)
    # 部
    department = models.ForeignKey(Department, on_delete=models.PROTECT)

    class Meta:
        db_table = "section"


class AffiliationHistoryManager(models.Manager):
    """所属履歴カスタムマネージャー"""
    def current(self):
        today = datetime.now().date()
        return self.get_queryset().filter(
            Q(end_on__gte=today) | Q(end_on__isnull=True),
            start_on__lte=today,
            is_deleted=False
        )


class AffiliationHistory(BaseModel):
    """所属履歴"""

    # 開始日
    start_on = models.DateField(null=True)
    # 終了日
    end_on = models.DateField(null=True)
    # ユーザー
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    # 部署
    section = models.ForeignKey(Section, on_delete=models.PROTECT)

    objects = AffiliationHistoryManager()

    class Meta:
        db_table = "affiliation_history"
