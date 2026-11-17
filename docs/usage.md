# 사용 가이드

[← SteSlide](../README.md) · [동작 구조](architecture.md) · [유지보수](maintenance.md)

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

일반 `git clone`으로 받았다면 `git submodule update --init --recursive`를 먼저 실행합니다.

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
