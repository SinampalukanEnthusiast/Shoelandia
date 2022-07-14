# Generated by Django 4.0.4 on 2022-07-09 09:23

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required. Must be unique', max_length=255, unique=True, verbose_name='Category Name')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Category safe URL')),
                ('is_active', models.BooleanField(default=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='store.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Required', max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text='Not Required', verbose_name='description')),
                ('slug', models.SlugField(max_length=255)),
                ('regular_price', models.DecimalField(decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 999.99.'}}, help_text='Maximum 999.99', max_digits=5, verbose_name='Regular price')),
                ('discount_price', models.DecimalField(decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 999.99.'}}, help_text='Maximum 999.99', max_digits=5, verbose_name='Discount price')),
                ('is_active', models.BooleanField(default=True, help_text='Change product visibility', verbose_name='Product visibility')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='store.category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='SubProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_name', models.CharField(help_text='Required. Sub-product Name', max_length=255, verbose_name='Subproduct Name')),
                ('brand', models.CharField(help_text='Shoe brand. Not required.', max_length=255, verbose_name='Brand Name')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_default', models.BooleanField(default=False, help_text='Is the main subproduct.', verbose_name='Flagship subproduct')),
                ('is_active', models.BooleanField(default=True, help_text='Change subproduct visibility', verbose_name='Subproduct visibility')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='store.product')),
            ],
            options={
                'verbose_name': 'Subproduct ',
                'verbose_name_plural': 'Subproducts',
            },
        ),
        migrations.CreateModel(
            name='ProductSizes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('EU16', 8.1), ('EU27', 16.1), ('EU28', 16.6), ('EU35', 21.2)], help_text='Sizes are in CM.', max_length=255, verbose_name='Subproduct Size')),
                ('stock_amount', models.IntegerField(default=0, help_text='Number of stock in inventory.', verbose_name='Stock amount.')),
                ('sub_product', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='store.subproduct')),
            ],
            options={
                'verbose_name': 'Product size ',
                'verbose_name_plural': 'Product sizes',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='images/default.png', help_text='Upload a product image', upload_to='images/', verbose_name='image')),
                ('alt_text', models.CharField(blank=True, help_text='Please add alternative text', max_length=255, null=True, verbose_name='Alterrnative text')),
                ('is_feature', models.BooleanField(default=False)),
                ('sub_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_image', to='store.subproduct')),
            ],
            options={
                'verbose_name': 'Subproduct Image',
                'verbose_name_plural': 'Subproduct Images',
            },
        ),
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('RD', 'Red'), ('BK', 'Black'), ('BL', 'Blue'), ('WT', 'White'), ('BR', 'Brown'), ('GR', 'Gray'), ('OR', 'Orange'), ('PN', 'Pink')], max_length=32, null=True, verbose_name='Subproduct Color')),
                ('stock_amount', models.IntegerField(default=0, help_text='Number of stock in inventory.', verbose_name='Stock amount.')),
                ('sub_product', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='store.subproduct')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryAttributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attributes', models.CharField(help_text='Characteristics of the category.', max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='store.category')),
            ],
        ),
        migrations.CreateModel(
            name='AttributeValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('values', models.CharField(help_text='Category attribute values.', max_length=255)),
                ('category_attributes', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='store.category')),
            ],
        ),
    ]
