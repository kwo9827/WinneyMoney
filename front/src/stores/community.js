import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from './accounts'

export const useCommunityStore = defineStore('community', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const articles = ref([]) // 게시글 리스트
  const comments = ref([]) // 댓글 리스트

  const accountStore = useAccountStore()
  // 게시글 목록 가져오기
  const getArticles = function (token) {
    console.log("현재 토큰:", accountStore.token) // 토큰 값 확인
    axios({
      method: 'get',
      url: `${API_URL}/articles/`,
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
      .then((res) => {
        console.log(res.data)
        articles.value = res.data
      })
      .catch((err) => {
        console.error('게시글 가져오기 실패:', err)
      })
  }

// 게시글 상세
const getArticleDetail = function (articleId) {
  const headers = accountStore.token
    ? { Authorization: `Token ${accountStore.token}` } // 토큰이 있는 경우에만 헤더 추가
    : {}; // 토큰이 없는 경우 빈 헤더

  return axios({
    method: 'get',
    url: `${API_URL}/articles/${articleId}/`,
    headers,
  })
    .then((res) => {
      console.log('게시글 상세 가져오기 성공:', res.data);
      return res.data;
    })
    .catch((err) => {
      console.error('게시글 상세 가져오기 실패:', err);
      throw err;
    });
};

  // 게시글 생성
  const createArticle = function (payload, token) {
    return axios({
      method: 'post',
      url: `${API_URL}/articles/`,
      data: {
        title: payload.title,
        content: payload.content,
      },
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
      .then((res) => {
        console.log('게시글 생성 성공:', res.data)
        articles.value.push(res.data)
        return res // 성공 응답 반환
      })
      .catch((err) => {
        console.error('게시글 생성 실패:', err)
        throw err // 에러를 호출한 곳으로 전달
      })
  }

// 게시글 수정
const updateArticle = function (articleId, payload) {
  return axios({
    method: 'put',
    url: `${API_URL}/articles/${articleId}/`,
    data: {
      title: payload.title,
      content: payload.content,
    },
    headers: {
      Authorization: `Token ${accountStore.token}`,
    },
  })
    .then((res) => {
      console.log('게시글 수정 성공:', res.data)
      const index = articles.value.findIndex((article) => article.id === articleId)
      if (index !== -1) {
        articles.value[index] = res.data
      }
      return res.data // 성공 응답 반환
    })
    .catch((err) => {
      console.error('게시글 수정 실패:', err)
      throw err // 에러를 호출한 곳으로 전달
    })
}


  // 게시글 삭제
  const deleteArticle = function (articleId) {
    return axios({ // <- 여기서 axios 호출 결과를 반환해야 함
      method: 'delete',
      url: `${API_URL}/articles/${articleId}/`,
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
      .then(() => {
        console.log('게시글 삭제 성공:', articleId);
        articles.value = articles.value.filter((article) => article.id !== articleId);
      })
      .catch((err) => {
        console.error('게시글 삭제 실패:', err);
        throw err; // 에러를 다시 호출한 쪽으로 전달
      });
  };

  // 댓글 조회
  const getComments = function (articleId) {
    return axios({
      method: 'get',
      url: `${API_URL}/articles/${articleId}/`,
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
      .then((res) => {
        comments.value = res.data.comments
        console.log('댓글 가져오기 성공:', comments.value)
        return comments.value
      })
      .catch((err) => {
        console.error('댓글 가져오기 실패:', err)
        throw err
      })
  }

  // 댓글 생성
  const createComment = function (articleId, payload, parentCommentId = null) {
    return axios({
      method: 'post',
      url: `${API_URL}/articles/comment/${articleId}/${parentCommentId ? parentCommentId : 0}/`,
      data: payload,
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
      .then((res) => {
        console.log('댓글 생성 성공:', res.data)
        return res.data
      })
      .catch((err) => {
        console.error('댓글 생성 실패:', err)
        throw err
      })
  } 

  // 댓글 삭제
  const deleteComment = function (articleId, commentId) {
    return axios({
      method: 'delete',
      url: `${API_URL}/articles/comment/${articleId}/${commentId}/delete/`,
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
      .then(() => {
        console.log('댓글 삭제 성공:', commentId)
        comments.value = comments.value.filter((comment) => comment.id !== commentId)
      })
      .catch((err) => {
        console.error('댓글 삭제 실패:', err)
        throw err
      })
  }

  // 댓글 수정
  const updateComment = function (commentId, payload) {
    return axios({
      method: 'put',
      url: `${API_URL}/articles/comment/${commentId}/update/`,
      data: payload,
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
      .then((res) => {
        console.log('댓글 수정 성공:', res.data)
        return res.data
      })
      .catch((err) => {
        console.error('댓글 수정 실패:', err)
        throw err
      })
  }

  return {
    articles,
    getArticles,
    createArticle,
    updateArticle,
    deleteArticle,
    getArticleDetail,
    getComments,
    createComment,
    deleteComment,
    updateComment,
  }
}, { persist: true,
})
