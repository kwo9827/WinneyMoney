# import openai

# def test_openai_api():
#     openai.api_key = "your-openai-api-key"  # 실제 API 키를 입력하거나 환경 변수로 가져옵니다.

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-4",  # 사용할 모델 이름
#             messages=[
#                 {"role": "system", "content": "You are the famous rapper. You are a helpful assistant. You always answer with the rhyme."},
#                 {"role": "user", "content": "Hello! How are you?"},
#             ],
#         )
#         print("응답 성공:")
#         print(response['choices'][0]['message']['content'])
#     except Exception as e:
#         print(f"OpenAI API 호출 오류: {e}")

# # 스크립트 실행
# if __name__ == "__main__":
#     test_openai_api()
