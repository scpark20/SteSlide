# SteSlide

채팅으로 Markdown과 CSS를 수정하고, 별도 브라우저나 VS Code에서 슬라이드 변화를 바로 확인하는 도구입니다. Lecture → Chapter → Section 파일을 합쳐 [Marp](https://github.com/marp-team/marp-cli)로 표시합니다.

강의 내용은 사용하는 프로젝트에, 공통 도구는 이 저장소에 둡니다. 기본 템플릿에는 강의 내용을 넣지 않았습니다.

## 프로젝트에 설치

Python 3.10 이상과 Git이 필요합니다. 프로젝트의 Git 저장소 루트에서 실행합니다.

```bash
git submodule add -b main https://github.com/scpark20/SteSlide.git tools/steslide
python3 tools/steslide/scripts/setup_marp.py
python3 tools/steslide/steslide.py init
python3 tools/steslide/steslide.py preview
```

브라우저에서 <http://localhost:8766/lecture.md>를 엽니다. 저장하면 자동 반영됩니다. 종료는 `Ctrl+C`입니다. 설치 스크립트는 공식 Marp CLI 4.5.1 실행 파일을 내려받고 SHA-256을 검증합니다. Node.js나 Python 패키지를 별도로 설치할 필요가 없습니다.

이미 Marp가 설치되어 있으면 설치 단계를 생략할 수 있습니다. `STESLIDE_MARP` 환경변수로 실행 파일 경로를 지정하거나 PATH의 `marp`를 사용합니다. 선택 순서는 환경변수 → 도구 내부 `.tools/marp/` → PATH입니다.

이미 SteSlide를 사용하는 프로젝트를 새로 받을 때는 다음과 같이 실행합니다.

```bash
git clone --recurse-submodules <프로젝트-저장소-URL>
cd <프로젝트-폴더>
python3 tools/steslide/scripts/setup_marp.py
python3 tools/steslide/steslide.py preview
```

일반 `git clone`으로 받았다면 `git submodule update --init --recursive`를 먼저 실행합니다. 비공개 저장소는 해당 GitHub 계정의 접근 권한이 필요합니다.

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

## 명령어

모든 명령은 사용하는 프로젝트 루트에서 실행합니다.

```bash
# 한 번 합치기 — Marp 없이도 가능
python3 tools/steslide/steslide.py build

# VS Code 미리보기용으로 합본만 계속 갱신
python3 tools/steslide/steslide.py watch

# 브라우저 미리보기
python3 tools/steslide/steslide.py preview --lecture lecture-01 --port 8766

# 내보내기
python3 tools/steslide/steslide.py export --format html
python3 tools/steslide/steslide.py export --format pdf
```

기본 결과는 `lectures/.build/lecture-01/lecture.html` 또는 `lecture.pdf`입니다. `--output 경로`로 변경합니다. PDF 변환에는 Chrome, Edge 또는 Firefox가 필요합니다. 자동 검색이 안 되면 `--browser firefox --browser-path /실행파일/경로`처럼 지정합니다.

다른 디렉터리에서 실행할 때는 명령 앞에 `--project /프로젝트/경로`를 넣습니다.

```bash
python3 /도구/경로/steslide.py --project /프로젝트/경로 preview
```

`init`은 없는 원본과 설정만 만들며 기존 파일을 덮어쓰지 않습니다. `.vscode/settings.json`이 이미 있으면 아래 테마 설정을 직접 합칩니다.

## VS Code와 Remote SSH

[Marp for VS Code](https://github.com/marp-team/marp-vscode)를 설치합니다. `watch`나 `preview`를 실행한 상태에서 `lecture.md` 또는 `chapter.md`를 열고 **Markdown: Open Preview to the Side**를 실행하면 하위 내용까지 보입니다. macOS 단축키는 `Cmd+K`, 이어서 `V`; Windows/Linux는 `Ctrl+K`, 이어서 `V`입니다.

```json
{
  "markdown.marp.themes": ["tools/steslide/theme.css"],
  "remote.portsAttributes": {
    "8766": {"label": "SteSlide", "onAutoForward": "openBrowser"}
  }
}
```

Remote SSH에서는 VS Code의 **Ports**에서 원격 `8766` 포트를 전달한 후 로컬 브라우저로 엽니다. 포트가 사용 중이면 `--port 8767`처럼 변경하고 해당 포트를 전달합니다. 브라우저에서는 `/lecture.md`로 전체 Lecture, `/chapter-01.md`로 해당 Chapter를 봅니다.

## 공통 도구 수정 → SteSlide에 반영

`tools/steslide`는 파일 복사본이 아니라 SteSlide 저장소입니다. 생성기·공통 테마·설치 도구의 수정은 이곳에서 커밋하고 SteSlide에 푸시합니다. 서브모듈을 새로 받으면 특정 커밋을 가리키므로 수정 전에 `main`으로 전환합니다.

```bash
git -C tools/steslide switch main
git -C tools/steslide pull --ff-only origin main
# tools/steslide 안의 필요한 파일 수정
python3 -m unittest discover -s tools/steslide/tests -v
git -C tools/steslide add <수정한-파일>
git -C tools/steslide commit -m "Describe the tool change"
git -C tools/steslide push origin main

# 사용하는 프로젝트에도 도구 버전을 기록
git add tools/steslide
git commit -m "Update SteSlide version"
git push
```

강의 내용은 `lectures/`에서 수정해 사용하는 프로젝트에 커밋합니다. 프로젝트 전용 테마가 필요하면 CSS를 프로젝트에 만들고 `steslide.json`의 `theme_file`에 그 상대 경로, `theme`에 CSS의 `@theme` 이름을 지정합니다. VS Code의 테마 경로도 맞춰 줍니다.

## SteSlide 업데이트 받기

서브모듈에 미커밋 변경이 없는 상태에서 실행합니다.

```bash
git submodule update --init --remote --merge tools/steslide
git add tools/steslide
git commit -m "Update SteSlide version"
git push
```

미리보기를 다시 시작하면 갱신된 Python 도구가 실행됩니다. 다른 사용자가 사용하는 프로젝트에 기록된 버전을 받을 때는 `git pull --recurse-submodules` 후 `git submodule update --init --recursive`를 실행합니다. Marp 버전이 바뀐 업데이트라면 `setup_marp.py`도 다시 실행합니다.

저장만으로 GitHub에 자동 푸시하지는 않습니다. 도구 수정은 SteSlide로, 도구 버전과 강의 수정은 사용하는 프로젝트로 커밋·푸시하는 구조입니다.

## 도구 자체 개발

```bash
git clone https://github.com/scpark20/SteSlide.git
cd SteSlide
python3 -m unittest discover -s tests -v
```

런타임은 Python 표준 라이브러리와 Marp CLI로 구성됩니다. 템플릿은 `templates/`, 공통 스타일은 `theme.css`, 생성기와 감시 코드는 `steslide.py`에 있습니다.
