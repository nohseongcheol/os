#!/usr/bin/env bash
# 사용: bash 압축하기.sh [저장할 파일.tar.gz]
# 기본 저장 위치: worldos 폴더 바로 위의 worldos.tar.gz
# 모든 하위 폴더에서 kernel*.iso를 제외하며 원본은 삭제하지 않습니다.
set -euo pipefail
umask 077
unset TAR_OPTIONS GZIP

if (( $# > 1 )); then
    printf '사용법: bash %s [저장할 파일.tar.gz]\n' "$0" >&2
    exit 1
fi

source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
source_parent=$(dirname -- "$source_dir")
source_name=$(basename -- "$source_dir")
archive=${1:-"$source_parent/$source_name.tar.gz"}
archive_dir=$(cd -- "$(dirname -- "$archive")" && pwd -P)
archive="$archive_dir/$(basename -- "$archive")"
partial="$archive.partial"

# 압축 파일 자체가 다시 압축에 포함되는 것을 방지합니다.
case "$archive" in
    "$source_dir"|"$source_dir"/*)
        printf '오류: 압축 파일은 %s 밖에 저장해 주세요.\n' "$source_dir" >&2
        exit 1
        ;;
esac

if [[ -e "$archive" || -L "$archive" || -e "$partial" || -L "$partial" ]]; then
    printf '오류: 기존 파일을 덮어쓰지 않습니다. 다른 저장 이름을 지정해 주세요.\n%s\n%s\n' \
        "$archive" "$partial" >&2
    exit 1
fi

printf '압축 대상: %s\n저장 위치: %s\n제외 이름: kernel*.iso (모든 하위 폴더)\n' \
    "$source_dir" "$archive"
printf '원본은 유지됩니다. VirtualBox 디스크도 포함되므로 관련 VM을 종료한 뒤 실행하는 것이 좋습니다.\n'

# 중간 .tar 파일 없이 곧바로 gzip 압축합니다.
# 따옴표는 *를 셸이 아닌 tar가 해석하도록 합니다.
# noclobber는 실행 도중 같은 이름의 파일이 생겨도 덮어쓰지 않게 합니다.
set -o noclobber
if ! tar --exclude='kernel*.iso' -zcvf - -C "$source_parent" -- "$source_name" > "$partial"; then
    printf '압축 실패: 원본은 유지되었습니다. 미완성 파일이 있으면 확인해 주세요: %s\n' "$partial" >&2
    exit 1
fi

if ! gzip -t -- "$partial"; then
    printf '압축 검사 실패: 미완성 파일을 확인해 주세요: %s\n' "$partial" >&2
    exit 1
fi

mv -n -T -- "$partial" "$archive"
if [[ -e "$partial" ]]; then
    printf '저장 이름이 이미 사용 중입니다. 압축 결과는 다음 파일에 보존했습니다: %s\n' "$partial" >&2
    exit 1
fi
printf '완료: %s\n원본 파일은 삭제하지 않았습니다.\n' "$archive"
