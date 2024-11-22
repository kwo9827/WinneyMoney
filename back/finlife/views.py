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

API_KEY = settings.DEPOSIT_API_KEY

# save_deposit_products requests 모듈을 활용하여 정기예금 상품 목록 데이터를 가져와 정기예금
# 상품 목록과 옵션 목록을 DB에 저장 GET
@api_view(['GET'])
def save_deposit_products(request):
    # 예금 url
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(url).json()
    baseLists = response.get('result').get('baseList')
    optionLists = response.get('result').get('optionList')
    # return Response(response)
    for baseList in baseLists:
        dcls_month = baseList.get('dcls_month') or -1
        fin_prdt_cd = baseList.get('fin_prdt_cd')
        kor_co_nm = baseList.get('kor_co_nm')
        fin_prdt_nm = baseList.get('fin_prdt_nm')
        join_way = baseList.get('join_way')
        mtrt_int = baseList.get('mtrt_int')
        spcl_cnd = baseList.get('spcl_cnd')
        join_deny = baseList.get('join_deny')
        join_member = baseList.get('join_member')
        etc_note = baseList.get('etc_note')
        max_limit = baseList.get('max_limit') or -1
        dcls_strt_day = baseList.get('dcls_strt_day') or -1
        dcls_end_day = baseList.get('dcls_end_day') or -1
        fin_co_subm_day = baseList.get('fin_co_subm_day') or -1

        if DepositProducts.objects.filter(dcls_month=dcls_month, 
                                          fin_prdt_cd=fin_prdt_cd, 
                                          kor_co_nm=kor_co_nm,
                                          fin_prdt_nm=fin_prdt_nm, 
                                          join_way=join_way, 
                                          mtrt_int=mtrt_int,
                                          spcl_cnd=spcl_cnd,
                                          join_deny=join_deny, 
                                          join_member=join_member, 
                                          etc_note=etc_note, 
                                          max_limit=max_limit,
                                          dcls_strt_day=dcls_strt_day,
                                          dcls_end_day=dcls_end_day,
                                          fin_co_subm_day=fin_co_subm_day
                                          ).exists(): continue

        save_data = {
            'dcls_month': dcls_month, 
            'fin_prdt_cd': fin_prdt_cd, 
            'kor_co_nm': kor_co_nm, 
            'fin_prdt_nm': fin_prdt_nm,
            'join_way': join_way,
            'mtrt_int': mtrt_int, 
            'spcl_cnd': spcl_cnd,
            'join_deny': join_deny, 
            'join_member': join_member, 
            'etc_note': etc_note, 
            'max_limit': max_limit,
            'dcls_strt_day': dcls_strt_day,
            'dcls_end_day': dcls_end_day,
            'fin_co_subm_day': fin_co_subm_day,
        }

        # return JsonResponse(save_data)
        serializer = DepositProductsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for optionList in optionLists :

        product_cd = optionList.get('fin_prdt_cd')
        product = DepositProducts.objects.get(fin_prdt_cd=product_cd)

        fin_prdt_cd = optionList.get('fin_prdt_cd')
        intr_rate_type_nm = optionList.get('intr_rate_type_nm')
        intr_rate = optionList.get('intr_rate') or -1
        intr_rate2 = optionList.get('intr_rate2')
        save_trm = optionList.get('save_trm')

        if DepositOptions.objects.filter(
            fin_prdt_cd=fin_prdt_cd, 
            intr_rate_type_nm=intr_rate_type_nm, 
            intr_rate=intr_rate, 
            intr_rate2=intr_rate2,
            save_trm=save_trm,
            ).exists():
            continue
    
        save_data = {
        'fin_prdt_cd' : fin_prdt_cd,
        'intr_rate_type_nm' : intr_rate_type_nm,
        'intr_rate' : intr_rate,
        'intr_rate2' : intr_rate2,
        'save_trm' : save_trm,
    }

        # return JsonResponse(save_data)
        serializer = DepositOptionsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(product=product)
            
    return JsonResponse({ 'message' : 'Okay!'})

@api_view(['GET'])
def save_saving_products(request):
    api_key = settings.DEPOSIT_API_KEY
    url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(url).json()
    baseLists = response.get('result').get('baseList')
    optionLists = response.get('result').get('optionList')
    for baseList in baseLists:
        dcls_month = baseList.get('dcls_month') or -1
        fin_prdt_cd = baseList.get('fin_prdt_cd')
        kor_co_nm = baseList.get('kor_co_nm')
        fin_prdt_nm = baseList.get('fin_prdt_nm')
        join_way = baseList.get('join_way')
        mtrt_int = baseList.get('mtrt_int')
        spcl_cnd = baseList.get('spcl_cnd')
        join_deny = baseList.get('join_deny')
        join_member = baseList.get('join_member')
        etc_note = baseList.get('etc_note')
        max_limit = baseList.get('max_limit') or -1
        dcls_strt_day = baseList.get('dcls_strt_day') or -1
        dcls_end_day = baseList.get('dcls_end_day') or -1
        fin_co_subm_day = baseList.get('fin_co_subm_day') or -1

        if SavingProducts.objects.filter(dcls_month=dcls_month, 
                                          fin_prdt_cd=fin_prdt_cd, 
                                          kor_co_nm=kor_co_nm, 
                                          fin_prdt_nm=fin_prdt_nm,
                                          join_way=join_way,
                                          mtrt_int=mtrt_int, 
                                          spcl_cnd=spcl_cnd,
                                          join_deny=join_deny, 
                                          join_member=join_member, 
                                          etc_note=etc_note, 
                                          max_limit=max_limit,
                                          dcls_strt_day=dcls_strt_day,
                                          dcls_end_day=dcls_end_day,
                                          fin_co_subm_day=fin_co_subm_day,
                                         ).exists(): continue

        save_data = {
            'dcls_month': dcls_month,  
            'fin_prdt_cd': fin_prdt_cd, 
            'kor_co_nm': kor_co_nm, 
            'fin_prdt_nm': fin_prdt_nm,
            'join_way': join_way,
            'mtrt_int': mtrt_int, 
            'spcl_cnd': spcl_cnd,
            'join_deny': join_deny, 
            'join_member': join_member, 
            'etc_note': etc_note, 
            'max_limit': max_limit,
            'dcls_strt_day': dcls_strt_day,
            'dcls_end_day': dcls_end_day,
            'fin_co_subm_day': fin_co_subm_day,
        }

        # return JsonResponse(save_data)
        serializer = SavingProductsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for optionList in optionLists :

        product_cd = optionList.get('fin_prdt_cd')
        product = SavingProducts.objects.get(fin_prdt_cd=product_cd)

        fin_prdt_cd = optionList.get('fin_prdt_cd')
        intr_rate_type_nm = optionList.get('intr_rate_type_nm')
        rsrv_type_nm = optionList.get('rsrv_type_nm')
        intr_rate = optionList.get('intr_rate') or -1
        intr_rate2 = optionList.get('intr_rate2')
        save_trm = optionList.get('save_trm')

        if SavingOptions.objects.filter(
            fin_prdt_cd=fin_prdt_cd, 
            intr_rate_type_nm=intr_rate_type_nm, 
            rsrv_type_nm=rsrv_type_nm,
            intr_rate=intr_rate, 
            intr_rate2=intr_rate2,
            save_trm=save_trm,
            ).exists():
            continue
    
        save_data = {
        'fin_prdt_cd' : fin_prdt_cd,
        'intr_rate_type_nm' : intr_rate_type_nm,
        'rsrv_type_nm' : rsrv_type_nm,
        'intr_rate' : intr_rate,
        'intr_rate2' : intr_rate2,
        'save_trm' : save_trm,
    }

        # return JsonResponse(save_data)
        serializer = SavingOptionsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(product=product)
            
    return JsonResponse({ 'message' : 'Okay!'})

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