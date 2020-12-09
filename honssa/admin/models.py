from django.db import models
from django.urls import reverse

# Create your models here.

class member_tbl(models.Model):
    member_join_date = models.DateTimeField(auto_now=True)
    member_manager = models.BooleanField(null=False, default=False)
    member_total_price = models.IntegerField(default=0)
    member_rank = models.CharField(max_length=20, default='VIP')
    member_password = models.CharField(max_length=15)
    member_id = models.CharField(max_length=18)
    member_contact_number = models.IntegerField()
    member_name = models.CharField(max_length=20)
    member_email = models.CharField(max_length=50)
    member_address = models.CharField(max_length=100)
    member_address_detail = models.CharField(max_length=100)
    member_discount = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('앱 네임:이름', args=[self.id])


class product_tbl(models.Model):
    product_Price = models.IntegerField(null=False)
    product_register_date = models.DateTimeField(auto_now=True)
    product_made_date = models.CharField(max_length=20)
    product_name = models.CharField(max_length=50, db_index=True)

    product_image = models.ImageField(upload_to='product', blank=True)
    product_description = models.CharField(max_length=1000, blank=True)
    product_volume = models.CharField(max_length=10)
    product_stock = models.IntegerField()
    product_category = models.CharField(max_length=20)
    product_size = models.CharField(max_length=20)
    product_brand = models.CharField(max_length=20)
    product_manufacturer = models.CharField(max_length=20)
    product_meterial = models.CharField(max_length=20)
    product_made_country = models.CharField(max_length=20)


class order_tbl(models.Model):
    member_id = models.ForeignKey(member_tbl, on_delete=models.CASCADE)
    product_id = models.ForeignKey(product_tbl, on_delete=models.CASCADE)
    order_price = models.IntegerField()
    order_pay_status = models.CharField(max_length=10, default='미결제')
    order_mathod = models.CharField(max_length=2)
    order_quantity = models.IntegerField()
    order_transport_number = models.CharField(max_length=50, default=0)
    order_bank = models.CharField(max_length=14)
    order_deposit_person = models.CharField(max_length=20)
    order_date = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length=6, default='미결제')
    order_delivery_company = models.CharField(max_length=20, default='준비중')


class cart_tbl(models.Model):
    member_number = models.ForeignKey(member_tbl, on_delete=models.CASCADE)
    product_number = models.ForeignKey(product_tbl, on_delete=models.CASCADE)
    cart_product_price = models.IntegerField()
    cart_quantity = models.IntegerField()


class m2mfaq_tbl(models.Model):
    member_number = models.ForeignKey(member_tbl, on_delete=models.CASCADE)
    comment_status = models.CharField(max_length=1, default=0)
    comment_image = models.ImageField(upload_to='m2m', max_length=100, null=True)
    comment_write_date = models.DateTimeField(auto_now=True)
    comment_title = models.CharField(max_length=50)
    comment_question = models.CharField(max_length=1000)
    comment_category = models.CharField(max_length=10)

    def get_absolute_url(self):
        return reverse('admin:m2m_answer', args=[self.id])


class faq_answer_tbl(models.Model):
    comment_number = models.ForeignKey(m2mfaq_tbl, on_delete=models.CASCADE)
    answer_description = models.CharField(max_length=1000)
    answer_write_date = models.DateTimeField(auto_now=True)
    answer_writer = models.CharField(max_length=3, default='관리자')


class address_tbl(models.Model):
    address_road_name = models.CharField(max_length=10)
    address_road_code = models.CharField(max_length=30)
    address_si_gun_gu = models.CharField(max_length=10)
    address_si_do = models.CharField(max_length=10)
    address_post_number = models.IntegerField()