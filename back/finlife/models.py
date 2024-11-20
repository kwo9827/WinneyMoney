from django.db import models
from django.conf import settings


# 예금 상품 
class DepositProducts(models.Model):
    dcls_month = models.CharField(max_length=6, blank=True, null=True)  # 공시 제출월(YYYYMM)
    fin_prdt_cd = models.TextField(unique=True)  # 금융 상품 코드
    kor_co_nm = models.TextField()  # 금융회사명
    fin_prdt_nm = models.TextField()  # 금융 상품명
    etc_note = models.TextField(blank=True, null=True)  # 금융 상품 설명
    join_deny = models.IntegerField(blank=True, null=True)  # 가입 제한
    join_member = models.TextField(blank=True, null=True)  # 가입대상
    join_way = models.TextField(blank=True, null=True)  # 가입 방법
    spcl_cnd = models.TextField(blank=True, null=True)  # 우대조건

    # favorited_by 필드: ManyToMany 관계
    favorited_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='UserFavoriteProducts',  # 중개 테이블 지정
        related_name='favorited_deposit_products',
        blank=True,
    )

    def __str__(self):
        return f"{self.kor_co_nm} - {self.fin_prdt_nm}"


# 예금 옵션
class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name='options')
    dcls_month = models.CharField(max_length=6, blank=True, null=True)  # 공시 제출월(YYYYMM)
    fin_prdt_cd = models.TextField()  # 금융 상품 코드
    intr_rate_type_nm = models.CharField(max_length=100)  # 저축금리 유형명
    intr_rate = models.FloatField()  # 저축금리
    intr_rate2 = models.FloatField()  # 최고우대금리
    save_trm = models.IntegerField()  # 저축기간 (단위: 개월)

    def __str__(self):
        return f"{self.product.fin_prdt_nm} - {self.save_trm}개월"


# 즐겨찾기한 상품들
class UserFavoriteProducts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_favorites')
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name='user_favorites')  # 관련 이름 변경
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # user, product 조합 고유 / 여러 번 즐겨 찾기 금지, 데이터 무결성 보장

    def __str__(self):
        return f"{self.user.username} - {self.product.fin_prdt_nm}"
