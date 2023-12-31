# Generated by Django 3.2 on 2023-07-06 15:28

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20230702_2205'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('code', models.IntegerField(unique=True)),
                ('order', models.IntegerField(unique=True)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
                ('updated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
            ],
            options={
                'db_table': 'brand',
            },
        ),
        migrations.CreateModel(
            name='Prefecture',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=10)),
                ('code', models.IntegerField(unique=True)),
                ('order', models.IntegerField(unique=True)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
                ('updated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
            ],
            options={
                'db_table': 'prefecture',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(default='', max_length=100)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.brand')),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
                ('prefecture', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.prefecture')),
                ('updated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
            ],
            options={
                'db_table': 'store',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(default='', max_length=254)),
                ('phone_no', models.IntegerField(null=True)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
                ('updated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
            ],
            options={
                'db_table': 'vendor',
            },
        ),
        migrations.CreateModel(
            name='StoreProduct',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.product')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.store')),
                ('updated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
            ],
            options={
                'db_table': 'store_product',
            },
        ),
        migrations.CreateModel(
            name='ProductRemarks',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('memo', models.TextField(default='')),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.product', unique=True)),
                ('updated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
            ],
            options={
                'db_table': 'product_remarks',
            },
        ),
        migrations.CreateModel(
            name='ProductInventory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('inventory', models.IntegerField()),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.product', unique=True)),
                ('updated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
            ],
            options={
                'db_table': 'product_inventory',
            },
        ),
        migrations.CreateModel(
            name='ProductImgPath',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('img_path', models.CharField(max_length=200)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.product', unique=True)),
                ('updated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
            ],
            options={
                'db_table': 'product_img_path',
            },
        ),
        migrations.CreateModel(
            name='ProductImgCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=50)),
                ('code', models.IntegerField(unique=True)),
                ('order', models.IntegerField(unique=True)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
                ('updated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
            ],
            options={
                'db_table': 'product_img_category',
            },
        ),
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('amount', models.IntegerField()),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.brand')),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.product', unique=True)),
                ('updated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main.vendor')),
            ],
            options={
                'db_table': 'product_detail',
            },
        ),
        migrations.CreateModel(
            name='product_category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=30)),
                ('code', models.IntegerField(unique=True)),
                ('order', models.IntegerField(unique=True)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
                ('updated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user')),
            ],
            options={
                'db_table': 'product_category',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.product_category'),
        ),
        migrations.AddField(
            model_name='product',
            name='created_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user'),
        ),
        migrations.AddField(
            model_name='product',
            name='updated_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.user'),
        ),
        migrations.AddConstraint(
            model_name='storeproduct',
            constraint=models.UniqueConstraint(fields=('store', 'product'), name='store_product_uniq'),
        ),
    ]
