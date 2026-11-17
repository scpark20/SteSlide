# 유지보수와 업데이트

[← SteSlide](../README.md) · [사용 가이드](usage.md) · [동작 구조](architecture.md)

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
