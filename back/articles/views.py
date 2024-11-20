from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import ArticleSerializer,CommentSerializer
from .models import Article,Comment


# 댓글 리스트 조회 및 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list(request):
    if request.method == 'GET':
        articles = get_list_or_404(Article)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

# 게시글 상세 조회
@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comments = Comment.objects.filter(article=article).order_by('created_at')
    if request.method == 'GET':
        article_serializer = ArticleSerializer(article)
        comment_serializer = CommentSerializer(comments, many=True)
        print('게시글', article_serializer.data)
        print('댓글', comment_serializer.data, article_pk)
        return Response({'article':article_serializer.data, 'comments':comment_serializer.data})
    
    if request.user != article.user:
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 댓글 생성
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comments_create(request, article_pk, parent_pk):
    article=get_object_or_404(Article,pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        if parent_pk:
            parent_Comment=get_object_or_404(pk=parent_pk)
            serializer.save(user=request.user, article=article, parent_comment=parent_Comment)
        else:
            serializer.save(user=request.user,article=article)
        return Response({'message':'success'})
    return Response({'message': 'fail'})


# 댓글 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comments_delete(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, article_id=article_pk, pk=comment_pk)
    if request.user != comment.user:
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# 댓글 수정
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def comment_update(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user != comment.user:
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CommentSerializer(comment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



