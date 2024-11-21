from django.db import models
from django.conf import settings


# 예금 상품 
class DepositProducts(models.Model):
    dcls_month = models.IntegerField(blank=True) # 공시 제출월 [YYYYMM]
    fin_prdt_cd = models.TextField(unique=True) # 금융상품 코드
    kor_co_nm = models.TextField() # 금융회사명
    fin_prdt_nm = models.TextField() #금융상품명
    join_way = models.TextField() #가입방법
    mtrt_int = models.TextField() # 만기 후 이자율
    spcl_cnd = models.TextField() #우대조건
    join_deny = models.IntegerField() #가입제한
    join_member = models.TextField() #가입대상
    etc_note = models.TextField() #기타유의사항
    max_limit = models.IntegerField(blank=True, null=True) # 최고한도
    dcls_strt_day = models.IntegerField(blank=True, null=True) # 공시 시작일
    dcls_end_day = models.IntegerField(blank=True, null=True) # 공시 종료일
    fin_co_subm_day = models.IntegerField(blank=True, null=True) # 금융회사 제출일 [YYYYMMDDHH24MI]

    # favorited_by 필드: ManyToMany 관계
    favorited_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='UserFavoriteDeposits',  # 중개 테이블 지정
        related_name='favorited_deposit_products',
        blank=True,
    )

    def __str__(self):
        return f"{self.kor_co_nm} - {self.fin_prdt_nm}"


# 예금 옵션
class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name='options') 
    fin_prdt_cd = models.TextField() #금융상품코드
    intr_rate_type_nm = models.CharField(max_length=100) #저축금리유형명
    intr_rate = models.FloatField() #저축금리
    intr_rate2 = models.FloatField() #최고우대금리
    save_trm = models.IntegerField() #저축기간

    def __str__(self):
        return f"{self.product.fin_prdt_nm} - {self.save_trm}개월"
    
#적금 상품
class SavingProducts(models.Model):
    dcls_month = models.IntegerField(blank=True) # 공시 제출월 [YYYYMM]
    fin_prdt_cd = models.TextField(unique=True) # 금융상품 코드
    kor_co_nm = models.TextField() # 금융회사명
    fin_prdt_nm = models.TextField() #금융상품명
    join_way = models.TextField() # 가입 방법
    mtrt_int = models.TextField() # 만기 후 이자율
    spcl_cnd = models.TextField() # 우대조건
    join_deny = models.IntegerField() #가입제한
    join_member = models.TextField() # 가입대상
    etc_note = models.TextField() # 기타 유의사항
    max_limit = models.IntegerField(blank=True, null=True) # 최고한도
    dcls_strt_day = models.IntegerField(blank=True, null=True) # 공시 시작일
    dcls_end_day = models.IntegerField(blank=True, null=True) # 공시 종료일
    fin_co_subm_day = models.IntegerField(blank=True, null=True) # 금융회사 제출일 [YYYYMMDDHH24MI]

    # favorited_by 필드: ManyToMany 관계
    favorited_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='UserFavoriteSavings',  # 중개 테이블 지정
        related_name='favorited_saving_products',
        blank=True,
    )

    def __str__(self):
        return f"{self.kor_co_nm} - {self.fin_prdt_nm}"
    
class SavingOptions(models.Model):
    product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE, related_name='options')
    fin_prdt_cd = models.TextField() #금융상품코드
    intr_rate_type_nm = models.CharField(max_length=100) #저축금리유형명
    rsrv_type_nm = models.CharField(max_length=100)
    intr_rate = models.FloatField() #저축금리
    intr_rate2 = models.FloatField() #최고우대금리
    save_trm = models.IntegerField() #저축기간

    def __str__(self):
        return f"{self.product.fin_prdt_nm} - {self.save_trm}개월"


# 즐겨찾기한 예금 상품들
class UserFavoriteDeposits(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorite_deposit_relations'  # 역참조 이름
    )
    deposit = models.ForeignKey(
        DepositProducts,
        on_delete=models.CASCADE,
        related_name='user_deposit_relations'  # 역참조 이름
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'deposit'], name='unique_user_deposit')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.deposit.fin_prdt_nm}"


# 즐겨찾기한 적금 상품들
class UserFavoriteSavings(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorite_saving_relations'  # 역참조 이름
    )
    saving = models.ForeignKey(
        SavingProducts,
        on_delete=models.CASCADE,
        related_name='user_saving_relations'  # 역참조 이름
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'saving'], name='unique_user_saving')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.saving.fin_prdt_nm}"
