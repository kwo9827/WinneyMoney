from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings

from .serializers import UserSerializer, ProfileSerializer, PasswordChangeSerializer
from finlife.models import DepositProducts

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

# 회원 상세 정보
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

# # 비밀번호 재설정 요청
# @api_view(['POST'])
# def password_reset_request(request):
#     email = request.data.get('email')
#     if not email:
#         return Response({'message': '이메일을 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
    
#     user = User.objects.filter(email=email).first()
#     if not user:
#         return Response({'message': '해당 이메일을 사용하는 사용자가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

#     token_generator = PasswordResetTokenGenerator()
#     token = token_generator.make_token(user)
#     uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
#     reset_url = f"{settings.FRONTEND_URL}/password-reset-confirm/{uidb64}/{token}/"
    
#     # 이메일 발송
#     send_mail(
#         subject="비밀번호 재설정 요청",
#         message=f"아래 링크를 클릭하여 비밀번호를 재설정하세요:\n{reset_url}",
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=[email],
#     )
#     return Response({'message': '비밀번호 재설정 이메일이 발송되었습니다.'}, status=status.HTTP_200_OK)

# # 비밀번호 재설정 확인
# @api_view(['POST'])
# def password_reset_confirm(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         return Response({'message': '유효하지 않은 요청입니다.'}, status=status.HTTP_400_BAD_REQUEST)

#     token_generator = PasswordResetTokenGenerator()
#     if not token_generator.check_token(user, token):
#         return Response({'message': '유효하지 않은 또는 만료된 토큰입니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
#     new_password = request.data.get('new_password')
#     if not new_password:
#         return Response({'message': '새 비밀번호를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
    
#     user.set_password(new_password)
#     user.save()
#     return Response({'message': '비밀번호가 성공적으로 변경되었습니다.'}, status=status.HTTP_200_OK)