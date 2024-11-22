from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, ProfileSerializer, PasswordChangeSerializer
from finlife.models import DepositProducts

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    # 현재 로그인한 사용자가 요청된 사용자를 팔로우하고 있는지 확인
    is_following = user.followers.filter(pk=request.user.pk).exists()
    serializer = ProfileSerializer(user, context={'request': request})
    return Response({
        'profile': serializer.data,
        'is_following': is_following, 
    }, status=status.HTTP_200_OK)

# 회원탈퇴
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({"message": "회원탈퇴가 성공적으로 처리되었습니다."}, status=status.HTTP_204_NO_CONTENT)

# 회원정보수정
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_user(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 비밀번호 변경
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = PasswordChangeSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        if user.check_password(serializer.validated_data['old_password']):
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': '비밀번호가 변경되었습니다.'}, status=status.HTTP_200_OK)
        return Response({'message': '현재 비밀번호가 틀립니다.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': '에러', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# 유저 팔로우 기능 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user == user_to_follow:
        return Response({'message': '자기 자신은 팔로우할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    if request.user.following.filter(username=username).exists():
        request.user.following.remove(user_to_follow)
        return Response({'message': f'{username} 팔로우 해제'}, status=status.HTTP_200_OK)
    else:
        request.user.following.add(user_to_follow)
        return Response({'message': f'{username} 팔로우'}, status=status.HTTP_200_OK)
    
# 즐겨찾기 추가/제거 기능
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, product_id):
    product = get_object_or_404(DepositProducts, id=product_id)
    user = request.user
    if user.favorite_products.filter(id=product_id).exists():
        user.favorite_products.remove(product)
        return Response({'message': '상품이 즐겨찾기에서 제거되었습니다.'}, status=status.HTTP_200_OK)
    else:
        user.favorite_products.add(product)
        return Response({'message': '상품이 즐겨찾기에 추가되었습니다.'}, status=status.HTTP_200_OK)

# 사용자의 즐겨찾기 목록 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_favorites(request):
    user = request.user
    serializer = ProfileSerializer(user, request=request)
    return Response(serializer.data['favorite_products'], status=status.HTTP_200_OK)