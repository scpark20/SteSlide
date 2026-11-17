# 동작 구조

[← SteSlide](../README.md) · [사용 가이드](usage.md) · [유지보수](maintenance.md)

## 편집과 미리보기 연결

```text
이 채팅에서 편집 요청
        ↓
프로젝트의 intro.md / section-*.md 또는 SteSlide의 theme.css 수정
        ↓ 저장 감지
chapter.md와 lecture.md 자동 생성
        ↓
Marp → 브라우저 슬라이드 자동 갱신
```

채팅 도구가 이 프로젝트 파일을 편집할 수 있어야 합니다. 사용자는 브라우저를 열어 둔 채 텍스트, 코드 블록, 표, 배치 변경을 요청합니다. SteSlide가 Python 에이전트를 실행하거나 `.py` 파일 내용을 자동 삽입하는 것은 아닙니다.

```text
사용하는 프로젝트/
├── tools/steslide/                   # 별도 Git 저장소인 서브모듈
├── steslide.json                     # 이 프로젝트의 공통 슬라이드 설정
└── lectures/
    ├── lecture-01/
    │   ├── intro.md                  # Lecture 첫 부분: 직접 편집
    │   ├── lecture.md                # 모든 Chapter 포함: 자동 생성
    │   └── chapter-01/
    │       ├── intro.md              # Chapter 첫 부분: 직접 편집
    │       ├── section-01.md         # Section 내용: 직접 편집
    │       └── chapter.md            # 모든 Section 포함: 자동 생성
    └── .build/lecture-01/            # 브라우저 미리보기·내보내기 결과
```

파일명 순서로 합칩니다. `chapter-01`, `chapter-02`와 `section-01.md`, `section-02.md`처럼 번호를 맞춥니다. 빈 파일은 합본에 빈 페이지를 추가하지 않습니다. 전부 비어 있으면 빈 화면 하나가 표시됩니다. Markdown 안의 `---`로 슬라이드를 나눕니다. 각 원본의 YAML 머리말은 합칠 때 제거하고 `steslide.json` 설정을 적용합니다. 슬라이드별 Marp 지시문(`<!-- _class: cover -->` 등)은 그대로 유지됩니다.

새 Chapter는 `chapter-02/intro.md`와 `section-01.md`를 만들면 됩니다. 새 Lecture는 `lecture-02/intro.md`부터 만들고 `--lecture lecture-02`로 선택합니다. 내용을 임의로 채우지 않고 사용자가 요청한 내용만 추가합니다.

## 생성과 감시

`steslide.py`는 Python 표준 라이브러리만 사용합니다. 원본을 모두 읽고 YAML 머리말을 제거한 다음 Chapter와 Lecture 합본을 만듭니다. 변경된 파일만 임시 파일을 거쳐 교체합니다. 해석할 수 없는 원본이 있으면 기존 합본을 유지합니다.

`watch`와 `preview`는 0.5초마다 원본·설정·테마의 변경을 확인합니다. 새 Section이나 삭제된 Chapter도 다음 합본에 반영합니다. `preview`는 Marp 서버를 함께 실행하며 브라우저 갱신은 Marp가 담당합니다. 종료할 때 함께 실행한 Marp 프로세스도 정리합니다.

## 설정과 파일 소유권

| 위치 | 역할 | 저장소 |
| --- | --- | --- |
| `intro.md`, `section-*.md` | 강의 원본 | 사용하는 프로젝트 |
| `steslide.json` | 테마·화면 비율·페이지 번호 설정 | 사용하는 프로젝트 |
| `steslide.py`, `theme.css` | 공통 생성기와 스타일 | SteSlide |
| `lecture.md`, `chapter.md`, `.build/` | 자동 생성된 미리보기 | Git에서 제외 |

합본의 전역 Marp 설정은 `steslide.json`을 따릅니다. 원본 파일을 단독으로 미리보기할 때는 그 파일의 YAML 머리말이 적용됩니다. 두 경로의 화면을 맞추려면 설정을 함께 유지합니다.
