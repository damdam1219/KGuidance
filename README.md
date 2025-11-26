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

K-Guidance는 **💜 K-contnet 💙를 중심으로 외국인 관광객들이 쉽고 간편하게 한국 여행을 계획하고 즐길 수 있도록 돕기 위해 개발된 맞춤형 K-여행 플래너 웹 서비스**입니다.

### 🔥 주요 기능 소개
![서비스기능소개](./docs/service_intro.png)
#### 1. **K-Content 기반 챗봇 – 맞춤형 여행지 추천**
📌 **사용자 선호 데이터를 기반으로 한 맞춤형 서울 여행지 추천 서비스**

**✔ 주요 기능**
- 사용자의 관심사·선호도 분석을 통한 추천  
- **K-콘텐츠 기반 추천 제공**
  - 🎵 K-pop 엔터테인먼트 스팟  
  - 🍽️ 연예인 인기 맛집  
  - 🎬 K-Drama 촬영지  
- 관심사 기반 RAG 모델로 컨텍스트 반영

**🛠 기술 스택**  
- **Qdrant 벡터 검색**  
- **RAG 기반 컨텍스트 추천 모델**

<details>
<summary>📸 해당 화면 보기 </summary>
<br/>
![챗봇 예시](./docs/chat_image1.png)
![챗봇 예시2](./docs/chat_image2.png)
</details>

---

#### 2. **K-Media 추천 시스템 – 한국 드라마 촬영지 기반 추천**
📌 **사용자가 좋아요(🧡)한 콘텐츠 기반으로 촬영지를 추천하는 개인화 시스템**

**✔ 주요 기능**
- 컨텐츠에 🧡 클릭 → 자동 북마크  
- 북마크된 콘텐츠 기반 **개인 맞춤 촬영지 추천**  
- 사용자 취향을 반영한 추천 근거까지 도출  

**✨ 차별점**
- “생각지도 못한 장소”를 발견하는 **서프라이즈 추천 시스템**

**🛠 기술 스택**
- **Qdrant 벡터 검색**
- **RAG 기반 추천 근거 생성 모델**

<details>
<summary>📸 화면 캡처 보기 (클릭)</summary>
<br/>
![추천 시스템 예시](./docs/recommend_1.png)
![추천 시스템 예시2](./docs/recommend_2.png)
</details>


#### 3. **사용자 일정 플래너 – 직관적인 일정 수정/관리 UI**
📌 **여행 일정 생성 → 지도 확인 → 대중교통 안내까지 한 번에 가능**

**✔ 주요 기능**
- 초보자도 쉽게 사용할 수 있는 직관적 일정 테이블  
- **지도 연동**으로 목적지 위치 실시간 확인  
- **대중교통(이동 경로) 자동 제공**

**✨ 차별점**
- 일정 확인/수정/삭제가 **한 화면**에서 모두 가능  
- 지도, 목적지 리스트, 일정 테이블이 연결된 **통합형 인터페이스**

**🛠 기술 스택**
- 🔍 **Google API** – 장소 검색  
- 🗺 **Naver Map API** – 영문 지도 제공  
- 🚇 **Odsay API** – 대중교통·환승 정보 제공

<details>
<summary>📸 화면 캡처 보기 (클릭)</summary>
<br/>
![일정 플래너 예시](./docs/planner_1.png)
![일정 플래너 예시2](./docs/planner_2.png)
</details>


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
