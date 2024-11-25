
# 📚 금융 프로젝트 (WinneyMoney)

**WinneyMoney**는 **금융상품 추천 서비스**를 제공하는 웹 애플리케이션입니다. 이 프로젝트는 **Vue.js**와 **Django**를 기반으로 백엔드와 프론트엔드를 분리 개발하였으며, 사용자 경험을 극대화하기 위해 **카카오 지도 API**와 **금융상품통합비교공시 API**를 활용하였습니다. 사용자가 손쉽게 금융 상품을 비교하고 추천받을 수 있도록 설계되었습니다.

---

## 👥 팀원 소개 및 역할 분담

| 역할 | 이름 및 GitHub 링크 | 주요 담당 업무 |
|------|--------------------|----------------|
| 백엔드 및 프론트엔드 | [오승열](https://github.com/kwo9827) | 회원 커스터마이징, 예적금 금리 비교, 커뮤니티 게시판, 프로필 |
| 백엔드 및 프론트엔드 | [김승윤](https://github.com/purekim333) | 환율 계산기, 은행 검색, 금융상품 추천 알고리즘, 포트폴리오 |

---

## 📅 개발 일정

| 날짜       | 작업 내용                                   |
|------------|--------------------------------------------|
| 2024.11.18 | 프로젝트 계획 및 기획 회의                 |
| 2024.11.19 | 프로젝트 초기 세팅 (Django & Vue.js 환경 구축), 회원가입 및 로그인 기능 구현 |
| 2024.11.20 | 금융 상품 게시판 페이지 구현, 카카오 지도 API 연동 |
| 2024.11.21 | 금융상품 추천 알고리즘 설계               |
| 2024.11.22 | 환율 계산기 구현                          |
| 2024.11.24 | 백엔드 API 구현 및 테스트                 |
| 2024.11.25 | 코드 개선 및 프론트엔드 UI/UX 디자인 개선  |
| 2024.11.26 | 최종 점검 및 배포                         |
| 2024.11.27 | 최종 발표                                 |

---

## 📌 주요 기능

- 금융 상품 추천 알고리즘을 활용하여 맞춤형 금융 상품 추천
- 예금 및 적금 금리 비교 기능 제공
- 사용자 회원가입/로그인/로그아웃/회원탈퇴 기능
- 커뮤니티 게시판을 통한 사용자 간 정보 공유
- **Vue.js**와 **Django** 기반의 프론트엔드 및 백엔드 분리 구조
- **카카오 지도 API**를 활용한 은행 위치 정보 제공
- 실시간 환율 계산 기능

---

## 🛠️ 기술 스택

- **Frontend:** Vue.js, JavaScript, Bootstrap
- **Backend:** Django, Django REST framework
- **Database:** SQLite (개발 단계)
- **API:** 카카오 지도 API, 금융상품통합비교공시 API, 한국수출입은행 API
- **Deployment:** 로컬 개발 환경 (향후 클라우드 서버 배포 예정)
- **Version Control:** Git, GitHub

---

## 🚀 설치 및 실행 방법

### 1. 프로젝트 클론
```bash
git clone https://github.com/your-github-id/FINLIFE.git
```

### 2. 백엔드 설정
```bash
cd back_fin
python -m venv venv
source venv/bin/activate  # 윈도우: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

### 3. 프론트엔드 설정
```bash
cd vue-project
npm install
npm run dev
```

---

## 💡 기여 방법

1. 이 레포지토리를 포크하세요.
2. 새로운 브랜치를 생성하세요.
   ```bash
   git checkout -b feature/my-feature
   ```
3. 변경 사항을 커밋하세요.
   ```bash
   git commit -m "Add some feature"
   ```
4. 브랜치에 푸시하세요.
   ```bash
   git push origin feature/my-feature
   ```
5. Pull Request를 제출하세요.

---

## 🏆 프로젝트의 핵심 가치는 무엇인가요?

**WinneyMoney**는 복잡한 금융 상품 비교 및 선택 과정을 간소화하고, 사용자가 자신에게 적합한 금융 상품을 쉽고 빠르게 찾을 수 있도록 돕습니다. 직관적인 사용자 인터페이스와 정확한 추천 시스템을 통해 사용자 경험을 극대화하는 것을 목표로 합니다.
