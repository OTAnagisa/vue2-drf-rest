import uuid
from datetime import datetime

from django.db import models
from django.db.models import Q, F
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
        return str(self.id)

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
    def current(self, includes_retired_last=False):
        """現在の所属履歴を取得するフィルター

        Parameters:
        ----------
        includes_retired_last: bool
            退職者の場合、最後の所属履歴を含むか
        """
        today = datetime.now().date()
        q = Q(
            Q(end_on__gte=today) | Q(end_on__isnull=True),
            start_on__lte=today,
            is_deleted=False,
        )

        if includes_retired_last:
            q |= Q(
                Q(end_on__gte=F("user__retirement_on")),
                Q(start_on__lte=F("user__retirement_on")),
            )
        return self.get_queryset().filter(q)


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


class ProductCategory(BaseModel):
    """商品カテゴリ"""

    # カテゴリ名
    name = models.CharField(max_length=30)
    # コード
    code = models.IntegerField(unique=True)
    # オーダー
    order = models.IntegerField(unique=True)

    class Meta:
        db_table = "product_category"


class Vendor(BaseModel):
    """業者"""

    # 業者名
    name = models.CharField(max_length=100)
    # メールアドレス
    email = models.EmailField(default="")
    # 電話番号
    phone_no = models.CharField(max_length=20, default="")
    # No
    no = models.IntegerField(unique=True)

    def save(self, *args, **kwargs):
        if not self.no:
            self.no = get_next_value("vendor_no")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "vendor"


class Product(BaseModel):
    """商品"""

    # 商品名
    name = models.CharField(max_length=50)
    # 商品カテゴリ
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    # No
    no = models.IntegerField(unique=True)

    def save(self, *args, **kwargs):
        if not self.no:
            self.no = get_next_value("product_no")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "product"


class ProductInventory(BaseModel):
    """商品在庫"""

    # 商品
    product = models.ForeignKey(Product, on_delete=models.PROTECT, unique=True)
    # 在庫数
    inventory = models.IntegerField()

    class Meta:
        db_table = "product_inventory"


class Prefecture(BaseModel):
    """県"""

    # 名前
    name = models.CharField(max_length=10)
    # コード
    code = models.IntegerField(unique=True)
    # オーダー
    order = models.IntegerField(unique=True)

    class Meta:
        db_table = "prefecture"


class Brand(BaseModel):
    """ブランド"""

    # ブランド名
    name = models.CharField(max_length=100)
    # No
    no = models.IntegerField(unique=True)

    def save(self, *args, **kwargs):
        if not self.no:
            self.no = get_next_value("brand_no")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "brand"


class Store(BaseModel):
    """店舗"""

    # 店舗名
    name = models.CharField(max_length=100, default="")
    # 県
    prefecture = models.ForeignKey(Prefecture, on_delete=models.PROTECT)
    # ブランド
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    # No
    no = models.IntegerField(unique=True)

    def save(self, *args, **kwargs):
        if not self.no:
            self.no = get_next_value("store_no")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "store"


class StoreProduct(BaseModel):
    """店舗商品紐づけ"""

    # 店舗
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    # 商品
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    class Meta:
        db_table = "store_product"
        constraints = [
            models.UniqueConstraint(
                fields=["store", "product"],
                name="store_product_uniq",
            ),
        ]


class ProductDetail(BaseModel):
    """商品詳細"""

    # 商品
    product = models.ForeignKey(Product, on_delete=models.PROTECT, unique=True)
    # 出品業者
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, null=True)
    # 金額
    amount = models.IntegerField()
    # ブランド
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)

    class Meta:
        db_table = "product_detail"


class ProductRemarks(BaseModel):
    """商品メモ"""

    # 商品
    product = models.ForeignKey(Product, on_delete=models.PROTECT, unique=True)
    # メモ
    memo = models.TextField(default="")

    class Meta:
        db_table = "product_remarks"


class ProductImgCategory(BaseModel):
    """商品画像カテゴリ"""

    # カテゴリ名
    name = models.CharField(max_length=50)
    # コード
    code = models.IntegerField(unique=True)
    # オーダー
    order = models.IntegerField(unique=True)

    class Meta:
        db_table = "product_img_category"


class ProductImgPath(BaseModel):
    """商品画像パス"""

    # 商品
    product = models.ForeignKey(Product, on_delete=models.PROTECT, unique=True)
    # 画像パス
    img_path = models.CharField(max_length=200)

    class Meta:
        db_table = "product_img_path"
