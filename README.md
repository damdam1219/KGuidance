# ✈ K-Guidance: 외국인을 위한 K-여행 가이드 서비스

> **저장소 주소:** https://github.com/damdam1219/KGuidance.git
> 
> **주최: [LG U+] Why Not SW Camp 7기**
> 
> **프로젝트 기간:** 2025.05.13 ~ 2025.11.21  
>  
> **세부 과정명: 클라우드 빅데이터 분석 & 실무 기반 서비스 개발 과정**

---

## 🖤 짱구같은 팀원소개 🖤
<table>
<tr>
  <td align="center">
    👉 <a href="https://github.com/damdam1219" target="_blank">
      <b>김다은(팀장)</b>
    </a>
  </td>
  <td align="center">
    👉 <a href="https://github.com/tmdstart" target="_blank">
      <b>백승범(팀원)</b>
    </a>
  </td>
  <td align="center">
    👉 <a href="https://github.com/meanresult" target="_blank">
      <b>한지훈(팀원)</b>
    </a>
  </td>
</tr>
  <tr>
    <td align="center"><img src="./wh07-3rd-kguidence/docs/da.png" alt="김다은" width="150"/></td>
    <td align="center"><img src="./wh07-3rd-kguidence/docs/se.png" alt="백승범" width="150"/></td>
    <td align="center"><img src="./wh07-3rd-kguidence/docs/gi.png" alt="한지훈" width="150"/></td>
  </tr>
  <tr>
    <td><b>역할:</b> 프론트엔드 개발/ UI·UX 기획</td>
    <td><b>역할:</b> 백엔드 개발/ API 설계</td>
    <td><b>역할:</b> 데이터베이스 관리 및 연동</td>
  </tr>
  <tr>
    <td><b>주요 기여:</b> 화면 설계, React 구조 구축, 지도·사용자 일정 플래너 설계</td>
    <td><b>주요 기여:</b> LLM 연동, 챗봇 개발, Qdrant 백엔드 구현, 배포 환경 구축</td>
    <td><b>주요 기여:</b> 데이터 수집 및 정제, 추천시스템 개발, Maria DB 데이터 설계</td>
  </tr>
</table>

---

## 💡 프로젝트 개요 (Project Overview)

K-Guidance는 ** 💜 K-contnet 💙를 중심으로 외국인 관광객들이 쉽고 간편하게 한국 여행을 계획하고 즐길 수 있도록 돕기 위해 개발된 맞춤형 K-여행 플래너 웹 서비스**입니다.

### 🔥 주요 기능 소개

### 1. **K-Content 기반 챗봇 – 맞춤형 여행지 추천**
- 사용자의 관심사·선호도 데이터를 분석하여 **맞춤형 한국(서울) 여행지**를 추천합니다.  
- **차별점:**  
  - K-콘텐츠 기반 추천  
  - K-pop 엔터테인먼트 스팟 추천  
  - 연예인 인기 맛집 추천  
  - K-Drama 촬영지 추천  
- **기술 스택:** Qdrant 벡터 검색 · RAG 기반 컨텍스트 추천 모델

---

### 2. **K-Media 추천 시스템 – 한국 드라마 촬영지 기반 추천**
- 사용자가 선택한 콘텐츠에 🧡(좋아요)를 누르면 자동으로 북마크에 저장됩니다.  
- 북마크된 콘텐츠를 기반으로 **개인화된 촬영지 추천**을 제공합니다.  
- **차별점:**  
  - 사용자가 예상하지 못한 목적지를 발견하는 재미 요소 제공  

---

### 3. **사용자 일정 플래너 – 직관적인 일정 수정·관리 테이블**
- 직관적인 UI로 처음 사용자도 쉽게 여행 일정을 만들 수 있습니다.  
- **지도 연동**을 통해 목적지 위치를 즉시 확인할 수 있습니다.  
- **대중교통 정보 제공**으로 이동 동선을 효율적으로 계획할 수 있습니다.  
- **차별점:**  
  - 일정 확인·수정·삭제 기능이 한 화면에서 즉시 가능  
  - 목적지, 지도, 일정 테이블이 연결된 통합 인터페이스
 
---

## 📚 프로젝트 문서 및 산출물

주요 기획 및 설계 문서를 링크합니다. (파일이 업로드된 경우)

* **프로젝트 기획서:** [링크]
* **WBS (작업 분할 구조):** [링크]
* **프로젝트 계획서:** [링크]

## 🏗️ 시스템 아키텍처 (System Architecture)

프로젝트 시스템의 전체 구조를 다이어그램이나 글로 설명합니다.

* **[개념 설명]:** [데이터 수집, 처리, 서비스 제공에 이르는 전체적인 파이프라인 설명]
* **기술 스택:**
    * **Frontend (프론트엔드):** [React/Vue.js/HTML, CSS, JavaScript]
    * **Backend (백엔드):** [Python Flask/Django, Node.js, Spring]
    * **Database (데이터베이스):** [MySQL, MongoDB, Qdrant 등]
    * **배포 환경:** [AWS EC2, Docker, Kubernetes 등]


## 📁 GitHub 저장소 및 파일 소개

본 저장소의 주요 폴더와 파일에 대한 간략한 설명입니다.

* `src/`: 서비스의 핵심 백엔드 및 프론트엔드 코드가 위치합니다.
* `ktravel_data/`: 데이터 전처리 및 분석에 사용된 Jupyter Notebook 파일들.
* `static/`: 프론트엔드 정적 파일 (이미지, CSS 등).
* `docs/`: 프로젝트 계획서, 기획서 등 문서 파일.
* `requirements.txt`: 프로젝트 실행에 필요한 Python 라이브러리 목록.

## 🖼️ 실제 화면 (Frontend Screenshots)

서비스의 주요 기능을 보여주는 실제 화면 사진을 삽입합니다. (최대 3~5장 권장)

### 메인 페이지


*설명: 서비스의 첫 화면 및 주요 탐색 기능*

### 여행 플래너 페이지


*설명: 사용자가 여행지를 추가하고 경로를 확인하는 화면*

### 맞춤 추천 결과 페이지


*설명: 사용자 입력 기반으로 추천된 여행지 목록*

## 💭 프로젝트 회고 (Retrospective)

### 1. 성공 요인

* [성공 요인 1]
* [성공 요인 2]

### 2. 어려웠던 점 및 극복 과정

* [어려웠던 기술적 난관 및 해결 과정]
* [팀원 간의 의견 충돌 및 조율 과정]

### 3. 배운 점 및 향후 계획

* [이 프로젝트를 통해 개인/팀이 배운 핵심 지식]
* [향후 서비스 발전 방향 또는 개선할 부분]
