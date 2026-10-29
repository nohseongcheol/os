#!/bin/sh
set -eu
# 외국어판의 이름을 Melayu 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for LALUAN in Path('legasi_sumber').rglob('*.java'):
    Nama = LALUAN.stem
    if not Nama.isidentifier() or unicodedata.normalize('NFC', Nama) != Nama:
        raise SystemExit('식별자 또는 menormalkan_VALUE RALAT: ' + str(LALUAN))
    SUMBER = LALUAN.read_text(encoding='utf-8')
    pengisytiharan_4f4f026b = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', SUMBER)
    if pengisytiharan_4f4f026b and pengisytiharan_4f4f026b.group(1) != Nama:
        raise SystemExit('Fail·공개 format_VALUE Nama 불일치: ' + str(LALUAN))
print('UTF-8 공개 format_VALUE·Fail Nama tentu_sahkan 완료; 현지어 검토 상태는 국가판 명명 data Rujukan')
PY
