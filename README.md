# 🐍 Python Study Repository

> Python 기초 문법부터 데이터 분석, GUI, 이미지 메타데이터(EXIF) 처리, Streamlit 기반 실전 프로젝트까지 단계별로 학습하고 실습한 코드를 모아둔 저장소입니다.  
> 학습 과정과 상세한 이론 설명은 **[raycho-dev 기술 블로그](https://raycho-dev.tistory.com/)**에 함께 연재되어 있습니다.

---

## 📑 목차 (Table of Contents)

1. [프로젝트 개요](#-프로젝트-개요)
2. [디렉토리 구조](#-디렉토리-구조)
3. [주요 학습 및 실습 내용](#-주요-학습-및-실습-내용)
   - [1. Python 기초 문법 (Basic)](#1-python-기초-문법-basic)
   - [2. Python GUI (Tkinter)](#2-python-gui-tkinter)
   - [3. 이미지 및 EXIF 메타데이터 처리](#3-이미지-및-exif-메타데이터-처리)
   - [4. [실전 프로젝트] 빌딩 관리 시스템 (BuildingManager)](#4-실전-프로젝트-빌딩-관리-시스템-buildingmanager)
4. [설치 및 실행 가이드](#-설치-및-실행-가이드)
5. [연계 블로그 포스팅 링크](#-연계-블로그-포스팅-링크)

---

## 📌 프로젝트 개요

- **목적**: 파이썬 프로그래밍의 기초부터 실생활 자동화 및 웹 대시보드 구축까지 단계별 학습
- **주요 기술 스택**:
  - **언어**: Python 3.x
  - **데이터 분석 및 DB**: Pandas, SQLite3
  - **웹 프레임워크**: Streamlit
  - **이미지 처리**: Pillow (PIL)
  - **GUI**: Tkinter

---

## 📂 디렉토리 구조

```plaintext
python_study/
├── BuildingManager/            # [실전 프로젝트] 빌딩 관리 시스템
│   ├── app.py                  # Streamlit 대시보드 웹 애플리케이션
│   ├── building.py             # 빌딩 기본 데이터 및 비즈니스 로직
│   ├── building_data.py        # SQLite DB 연동 및 CRUD 함수
│   ├── building_manager.db     # 입주사/수익 관리 SQLite 데이터베이스
│   ├── building_padas.py       # Pandas 기반 임대료 정산 및 분석
│   └── monthly_building_report.csv # 월별 임대/관리비 정산 리포트
│
├── exif_Tag/                   # EXIF 태그 기반 사진 자동 분류
│   ├── exif_photo_auto.py      # 사진 촬영 날짜 기준 디렉토리 자동 생성 및 분류
│   ├── exif_tag_date.py        # 촬영 일자 추출 스크립트
│   ├── exif_tag_info.py        # 전체 EXIF 태그 정보 파싱
│   └── photo_date.py           # 파일 시간 정보 확인 예제
│
├── GUI001.py                   # Tkinter 클래스 기반 기본 윈도우 및 버튼 이벤트
├── GUI002.py                   # Tkinter 창 크기, 위치 및 리사이즈 옵션 제어
├── exif_tag1.py                # Pillow 라이브러리를 활용한 기본 EXIF 추출
├── time_conv.py                # 타임스탬프 포맷 변환 예제
├── study_001.py ~ study_008.py # 파이썬 기본 입출력, 연산, 조건문, 수학/이미지 예제
└── README.md                   # 스터디 정리 문서
```

---

## 💡 주요 학습 및 실습 내용

### 1. Python 기초 문법 (Basic)
기본적인 파이썬 문법과 표준 라이브러리 활용 예제입니다.

| 파일명 | 주요 내용 |
| :--- | :--- |
| `study_001.py` | 변수 선언, 문자열 출력 및 반복 연산 |
| `study_002.py` | `print()` 줄바꿈 제어 (`end` 옵션) |
| `study_003.py` | `if` 조건문 기초 |
| `study_004.py` | 문자열 포맷팅 및 구분선 출력 |
| `study_005.py` | `math` 모듈을 활용한 원 면적 계산 |
| `study_006.py` | 삼각함수 (`math.sin`, `cos`, `tan`) 및 각도/라디안 변환 |
| `study_007.py` | 조건 분기 처리를 활용한 BMI(체질량지수) 계산기 |
| `study_008.py` | Pillow(`PIL.Image`)를 통한 이미지 포맷, 모드, 해상도 확인 |
| `time_conv.py` | `time.strftime()`을 이용한 타임스탬프 포맷 변환 |

### 2. Python GUI (Tkinter)
파이썬 기본 내장 모듈인 `tkinter`를 사용하여 윈도우 어플리케이션을 구현했습니다.

- **`GUI001.py`**: 객체지향(OOP) 구조로 창을 생성하고, 메시지박스(`messagebox.showinfo`) 이벤트 바인딩
- **`GUI002.py`**: 윈도우 크기 지정(`geometry`), 위치 좌표 설정 및 창 크기 조절 제한(`resizable(False, False)`)

### 3. 이미지 및 EXIF 메타데이터 처리
사진의 메타데이터(EXIF)를 읽고, 촬영일자별로 사진을 자동 정리하는 도구입니다.

- **`exif_tag1.py` / `exif_Tag/exif_tag_info.py`**: 디지털 사진의 태그 번호를 사람이 읽을 수 있는 키값으로 디코딩
- **`exif_Tag/exif_photo_auto.py`**: 
  - 사진 폴더 내 파일들을 탐색하여 EXIF 내 촬영 날짜(`DateTimeOriginal`)를 파싱
  - 연/월/일 기준 폴더를 자동 생성하고 사진을 이동/분류하여 대량 사진 정리 자동화

### 4. [실전 프로젝트] 빌딩 관리 시스템 (BuildingManager)
> **"내 손으로 만드는 빌딩 관리 시스템 구축 프로젝트"**  
> 입주사 관리, 관리비/공과금 자동 계산, 임대 수익 분석을 웹 대시보드로 원스톱 제공하는 토이 프로젝트입니다.

- **DB CRUD (`building_data.py`)**: SQLite 연동으로 입주 호수, 상호명, 계약 기간, 보증금, 월세 등 CRUD 기능 구현
- **정산 분석 (`building_padas.py`)**: Pandas DataFrame을 활용하여 관리비·전기세 연동 계산 및 월별 수익 리포트 CSV 생성
- **웹 대시보드 (`app.py`)**: Streamlit을 이용해 10분 만에 상호작용 가능한 웹 모니터링 UI 구축

---

## 🚀 설치 및 실행 가이드

### 1) 필수 라이브러리 설치
```bash
pip install pandas streamlit pillow
```

### 2) 빌딩 관리 대시보드 실행
```bash
cd BuildingManager
streamlit run app.py
```

### 3) 사진 자동 분류기 실행
```bash
python exif_Tag/exif_photo_auto.py
```

---

## 🔗 연계 블로그 포스팅 링크

각 소스코드와 관련된 상세 해설은 아래 티스토리 블로그 링크를 참고하세요.

| 카테고리 | 주제 / 글 제목 | 블로그 링크 |
| :--- | :--- | :--- |
| **Python 기초** | Python 소개 및 환경 | [포스팅 보기](https://raycho-dev.tistory.com/70) |
| **Python 기초** | Python 공부하면서 만들어본 기초 소스 | [포스팅 보기](https://raycho-dev.tistory.com/118) |
| **개발 환경** | Google Drive Colab 설정 및 활용 가이드 | [포스팅 보기](https://raycho-dev.tistory.com/74) |
| **GUI** | Python GUI 라이브러리 Tkinter 활용법 | [포스팅 보기](https://raycho-dev.tistory.com/77) |
| **이미지/EXIF** | Image info / EXIF tag 정보 읽어오기 | [포스팅 보기](https://raycho-dev.tistory.com/72) |
| **이미지/EXIF** | EXIF 정보를 활용하여 날짜별 사진 자동 분류 | [포스팅 보기](https://raycho-dev.tistory.com/181) |
| **빌딩 관리기 (1)** | 빌딩 관리 시스템 구축 가이드 개요 | [포스팅 보기](https://raycho-dev.tistory.com/168) |
| **빌딩 관리기 (2)** | SQLite DB 연동 및 입주사 정보 CRUD 구현 | [포스팅 보기](https://raycho-dev.tistory.com/169) |
| **빌딩 관리기 (3)** | Pandas로 관리비·공과금 자동 계산 및 임대 수익 분석 | [포스팅 보기](https://raycho-dev.tistory.com/170) |
| **빌딩 관리기 (4)** | Streamlit으로 10분 만에 웹 대시보드 완성하기 | [포스팅 보기](https://raycho-dev.tistory.com/171) |
