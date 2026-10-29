# 이전 코드를 old에 보관하고 golang/worldos 올리기

현재 `/home/user/golang/worldos`에는 `.git`이 없다. **기존 GitHub 저장소를 별도 디렉터리에 복제한 다음 그 복제본에서 작업**하면 기존 Git 이력을 이어갈 수 있다. 아래의 `사용자명/저장소명`만 실제 주소로 바꾼다. 아래 명령은 안내이며 자동 실행하지 않았다.

2026-09-13의 읽기 전용 미리보기에서 원본 전체는 약 8.6GB였고, 아래 제외 규칙을 적용한 업로드 대상은 일반 파일 71,271개·350,229,076바이트(약 334MiB)였다. 소스가 변경되면 이 수치도 달라진다.

업로드 후 구조:

```text
저장소/
├── old/이동시각/          # 이전 저장소의 파일
├── golang/worldos/      # 현재 소스
└── .gitignore
```

1. 기존 GitHub 저장소를 복제하고 작업 브랜치를 만든다. 아래는 Bash용이다.

```bash
upload_dir=$(mktemp -d /home/user/worldos-upload.XXXXXX)
git clone https://github.com/사용자명/저장소명.git "$upload_dir" || exit 1
cd "$upload_dir" || exit 1
git checkout -b archive-and-upload-worldos || exit 1
```

2. Git이 추적하는 이전 파일을 `old/이동시각/`으로 이동한다. `.git` 내부는 대상이 아니며, 기존 `old` 폴더는 보존한다. 기존 `.github`도 이전 코드와 함께 보관되므로 그 안의 워크플로는 새 위치에서 실행되지 않는다.

```bash
archive_dir="old/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$archive_dir"
git ls-tree -z --name-only HEAD |
while IFS= read -r -d '' item; do
    [ "$item" = old ] && continue
    git mv -- "$item" "$archive_dir/$item" || exit 1
done

git diff --cached --stat
# 위 이동에 오류가 없다면:
git commit -m "Archive previous source under old"
```

`git mv`는 이동 결과를 스테이징한다. 이동을 별도 커밋으로 남기면 변경 경위를 보기 쉽다. [Git 공식 문서](https://git-scm.com/docs/git-mv)

3. 현재 소스를 복사한다. 생성된 실행 이미지·빌드 결과는 제외한다. 아래 명령은 원본 `/home/user/golang/worldos`를 변경하지 않는다.

```bash
mkdir -p golang/worldos
rsync -a \
  --exclude='.git/' \
  --exclude='build/' \
  --exclude='build-verification/' \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  --exclude='*.iso' \
  --exclude='*.img' \
  --exclude='*.vdi' \
  --exclude='*.qcow2' \
  --exclude='*.vmdk' \
  /home/user/golang/worldos/ golang/worldos/

cat > .gitignore <<'EOF'
/golang/worldos/**/build/
/golang/worldos/**/build-verification/
/golang/worldos/**/__pycache__/
/golang/worldos/**/*.pyc
/golang/worldos/**/*.iso
/golang/worldos/**/*.img
/golang/worldos/**/*.vdi
/golang/worldos/**/*.qcow2
/golang/worldos/**/*.vmdk
EOF
```

4. 추가할 파일을 확인한 뒤 커밋하고 작업 브랜치를 업로드한다.

```bash
find golang/worldos -type f -size +100M -print
git add .gitignore golang/worldos
git diff --cached --stat
git status --short
# 파일 목록과 크기 확인 후:
git commit -m "Add current golang/worldos source"
git push -u origin archive-and-upload-worldos
```

GitHub 일반 Git 업로드는 파일 하나가 100 MiB를 초과하면 차단된다. 위 큰 파일 검색 결과가 있으면 커밋 전에 확인하고, 실행 이미지 등은 GitHub Releases나 Git LFS에 별도로 올린다. [GitHub 파일 크기 제한](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)

5. GitHub 저장소에서 방금 올린 `archive-and-upload-worldos` 브랜치의 **Compare & pull request**를 선택하고 기본 브랜치로 병합한다. 병합 후 기본 브랜치에 `old/`와 `golang/worldos/`가 표시된다. 기본 브랜치 이름이 `main`인지 `master`인지 이 절차에서 가정하지 않는다.

현재 소스를 저장소 최상위에 두려면 3단계의 복사 대상 `golang/worldos/`를 `./`로 바꾸고 `.gitignore`의 경로 접두어도 그에 맞게 조정한다. 위 본문은 사용자가 지정한 `golang/worldos` 경로를 유지하는 방식이다.

HTTPS로 push할 때 인증을 요청하면 GitHub 계정 비밀번호 대신 개인 액세스 토큰을 사용한다. GitHub CLI가 설치되어 있으면 `gh auth login`으로 브라우저 인증을 설정할 수도 있다. [GitHub 공식 인증 안내](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github)
