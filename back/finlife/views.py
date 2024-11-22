from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from .models import DepositProducts, DepositOptions, SavingOptions, SavingProducts, UserFavoriteDeposits, UserFavoriteSavings
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, SavingOptionsSerializer, SavingProductsSerializer
from django.conf import settings
import requests
from django.http import JsonResponse
from django.db import IntegrityError
from django.db.models import Q

API_KEY = settings.DEPOSIT_API_KEY

# save_deposit_products requests 모듈을 활용하여 정기예금 상품 목록 데이터를 가져와 정기예금
# 상품 목록과 옵션 목록을 DB에 저장 GET
@api_view(['GET'])
def save_deposit_products(request):
    # API 요청
    url = f"http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1"
    response = requests.get(url).json()
    baseLists = response.get('result', {}).get('baseList', [])
    optionLists = response.get('result', {}).get('optionList', [])

    # 예금 상품 저장
    for base in baseLists:
        try:
            product, created = DepositProducts.objects.get_or_create(
                fin_prdt_cd=base.get('fin_prdt_cd'),
                defaults={
                    'dcls_month': base.get('dcls_month') or -1,
                    'kor_co_nm': base.get('kor_co_nm'),
                    'fin_prdt_nm': base.get('fin_prdt_nm'),
                    'join_way': base.get('join_way'),
                    'mtrt_int': base.get('mtrt_int'),
                    'spcl_cnd': base.get('spcl_cnd'),
                    'join_deny': base.get('join_deny'),
                    'join_member': base.get('join_member'),
                    'etc_note': base.get('etc_note'),
                    'max_limit': base.get('max_limit') or -1,
                    'dcls_strt_day': base.get('dcls_strt_day') or -1,
                    'dcls_end_day': base.get('dcls_end_day') or -1,
                    'fin_co_subm_day': base.get('fin_co_subm_day') or -1,
                }
            )
            if created:
                print(f"새 예금 상품 저장: {product.fin_prdt_cd}")
        except IntegrityError as e:
            print(f"예금 상품 저장 오류: {e}")

    # 예금 옵션 저장
    for option in optionLists:
        try:
            product = DepositProducts.objects.get(fin_prdt_cd=option.get('fin_prdt_cd'))
            option_data = {
                'product': product,
                'fin_prdt_cd': option.get('fin_prdt_cd'),
                'intr_rate_type_nm': option.get('intr_rate_type_nm'),
                'intr_rate': option.get('intr_rate') or -1,
                'intr_rate2': option.get('intr_rate2') or -1,
                'save_trm': option.get('save_trm'),
            }
            _, created = DepositOptions.objects.get_or_create(
                product=product,
                fin_prdt_cd=option_data['fin_prdt_cd'],
                intr_rate_type_nm=option_data['intr_rate_type_nm'],
                save_trm=option_data['save_trm'],
                defaults=option_data
            )
            if created:
                print(f"새 예금 옵션 저장: {option_data['fin_prdt_cd']} - {option_data['save_trm']}개월")
        except DepositProducts.DoesNotExist:
            print(f"예금 상품 없음: {option.get('fin_prdt_cd')}")
        except IntegrityError as e:
            print(f"예금 옵션 저장 오류: {e}")

    return Response({"message": "Deposit products and options saved successfully."}, status=status.HTTP_200_OK)


@api_view(['GET'])
def save_saving_products(request):
    # API 요청
    url = f"http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1"
    response = requests.get(url).json()
    baseLists = response.get('result', {}).get('baseList', [])
    optionLists = response.get('result', {}).get('optionList', [])

    # 적금 상품 저장
    for base in baseLists:
        try:
            product, created = SavingProducts.objects.get_or_create(
                fin_prdt_cd=base.get('fin_prdt_cd'),
                defaults={
                    'dcls_month': base.get('dcls_month') or -1,
                    'kor_co_nm': base.get('kor_co_nm'),
                    'fin_prdt_nm': base.get('fin_prdt_nm'),
                    'join_way': base.get('join_way'),
                    'mtrt_int': base.get('mtrt_int'),
                    'spcl_cnd': base.get('spcl_cnd'),
                    'join_deny': base.get('join_deny'),
                    'join_member': base.get('join_member'),
                    'etc_note': base.get('etc_note'),
                    'max_limit': base.get('max_limit') or -1,
                    'dcls_strt_day': base.get('dcls_strt_day') or -1,
                    'dcls_end_day': base.get('dcls_end_day') or -1,
                    'fin_co_subm_day': base.get('fin_co_subm_day') or -1,
                }
            )
            if created:
                print(f"새 적금 상품 저장: {product.fin_prdt_cd}")
        except IntegrityError as e:
            print(f"적금 상품 저장 오류: {e}")

    # 적금 옵션 저장
    for option in optionLists:
        try:
            product = SavingProducts.objects.get(fin_prdt_cd=option.get('fin_prdt_cd'))
            option_data = {
                'product': product,
                'fin_prdt_cd': option.get('fin_prdt_cd'),
                'intr_rate_type_nm': option.get('intr_rate_type_nm'),
                'rsrv_type_nm': option.get('rsrv_type_nm'),
                'intr_rate': option.get('intr_rate') or -1,
                'intr_rate2': option.get('intr_rate2') or -1,
                'save_trm': option.get('save_trm'),
            }
            _, created = SavingOptions.objects.get_or_create(
                product=product,
                fin_prdt_cd=option_data['fin_prdt_cd'],
                intr_rate_type_nm=option_data['intr_rate_type_nm'],
                save_trm=option_data['save_trm'],
                defaults=option_data
            )
            if created:
                print(f"새 적금 옵션 저장: {option_data['fin_prdt_cd']} - {option_data['save_trm']}개월")
        except SavingProducts.DoesNotExist:
            print(f"적금 상품 없음: {option.get('fin_prdt_cd')}")
        except IntegrityError as e:
            print(f"적금 옵션 저장 오류: {e}")

    return Response({"message": "Saving products and options saved successfully."}, status=status.HTTP_200_OK)

# deposit_products GET: 전체 정기예금 상품 목록 반환
# POST: 상품 데이터 저장 GET, POST
@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'GET':
        deposit_products = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(deposit_products, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET',])
def deposit_detail(request, product_id):
    print('호출')
    deposit = DepositProducts.objects.get(id=product_id)
    serializer = DepositProductsSerializer(deposit)
    return Response(serializer.data)


# deposit_product_options 특정 상품의 옵션 리스트 반환 GET
@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    print(f"요청 받은 상품 코드: {fin_prdt_cd}")  # 디버깅용 출력
    # fin_prdt_cd로 데이터 조회
    depositoptions = DepositOptions.objects.filter(product__fin_prdt_cd=fin_prdt_cd)
    print(f"조회된 옵션 개수: {depositoptions.count()}")  # 디버깅용 출력
    serializer = DepositOptionsSerializer(depositoptions, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def saving_products(request):
    if request.method == 'GET' :
        savings = SavingProducts.objects.all()
        serializer = SavingProductsSerializer(savings, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST' :
        serializer = SavingProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
@api_view(['GET',])
def saving_detail(request, product_id):
    print('호출')
    deposit = SavingProducts.objects.get(id=product_id)
    print(product_id, deposit)
    serializer = SavingProductsSerializer(deposit)
    return Response(serializer.data)


# 예금 상품 즐겨찾기 추가, 제거
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def favorite_deposit(request, fin_prdt_cd):
    product = get_object_or_404(DepositProducts, fin_prdt_cd=fin_prdt_cd)
    favorite, created = UserFavoriteDeposits.objects.get_or_create(user=request.user, deposit=product)
    if not created:
        favorite.delete()
        return Response({"message": "예금 상품이 즐겨찾기에서 제거되었습니다."}, status=status.HTTP_200_OK)
    return Response({"message": "예금 상품이 즐겨찾기에 추가되었습니다."}, status=status.HTTP_201_CREATED)


# 적금 상품 즐겨찾기 추가, 제거
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def favorite_saving(request, fin_prdt_cd):
    product = get_object_or_404(SavingProducts, fin_prdt_cd=fin_prdt_cd)
    favorite, created = UserFavoriteSavings.objects.get_or_create(user=request.user, saving=product)
    if not created:
        favorite.delete()
        return Response({"message": "적금 상품이 즐겨찾기에서 제거되었습니다."}, status=status.HTTP_200_OK)
    return Response({"message": "적금 상품이 즐겨찾기에 추가되었습니다."}, status=status.HTTP_201_CREATED)


# 현재 유저의 즐겨찾기 목록 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_favorites(request):
    # 현재 유저가 즐겨찾기한 예금 상품
    favorites_deposit = DepositProducts.objects.filter(favorited_by_users__user=request.user)
    # 현재 유저가 즐겨찾기한 적금 상품
    favorites_saving = SavingProducts.objects.filter(favorited_by_users__user=request.user)

    deposit_serializer = DepositProductsSerializer(favorites_deposit, many=True, context={'request': request})
    saving_serializer = SavingProductsSerializer(favorites_saving, many=True, context={'request': request})

    result = {
        'favorite_deposit': deposit_serializer.data,
        'favorite_saving': saving_serializer.data
    }

    return Response(result, status=status.HTTP_200_OK)