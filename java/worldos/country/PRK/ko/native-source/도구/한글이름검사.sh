#!/bin/sh
set -eu

# JVM이 강제하는 main과 Java 표준 형식 이름은 허용한다. 프로젝트가 소유한
# 공개 형식/메서드/필드 이름에 영문만 사용한 경우에는 빌드를 중단한다.
if find 원천 -type f -name '*.java' -printf '%f\n' | grep -Ev '^[가-힣0-9_]+\.java$' >/dev/null; then
    echo '영문 Java 파일 이름을 발견했습니다.' >&2
    exit 1
fi

if grep -RInE '^[[:space:]]*(public|protected|private)?[[:space:]]*(static[[:space:]]+)?(final[[:space:]]+)?(class|interface|enum)[[:space:]]+[A-Za-z][A-Za-z0-9_]*' 원천 >/dev/null; then
    echo '영문으로만 된 소유 형식 이름을 발견했습니다.' >&2
    exit 1
fi

if grep -RInE '^[[:space:]]*(public|protected|private)[[:space:]]+([^()]|\([^)]*\))*[[:space:]][A-Za-z][A-Za-z0-9_]*[[:space:]]*\(' 원천 \
        | grep -v '=' \
        | grep -Ev '[[:space:]]main[[:space:]]*\(' >/dev/null; then
    echo '영문으로만 된 소유 메서드 이름을 발견했습니다.' >&2
    exit 1
fi

echo '한글 이름 검사: 통과'
