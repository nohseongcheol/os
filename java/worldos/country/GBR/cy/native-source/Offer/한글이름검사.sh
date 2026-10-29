#!/bin/sh
set -eu
# 외국어판의 이름을 Cymraeg 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for LLWYBR in Path('hen_ffynhonnell').rglob('*.java'):
    Enw = LLWYBR.stem
    if not Enw.isidentifier() or unicodedata.normalize('NFC', Enw) != Enw:
        raise SystemExit('dynodwr_VALUE 또는 normaleiddio_VALUE Gwall: ' + str(LLWYBR))
    FFYNHONNELL = LLWYBR.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', FFYNHONNELL)
    if 선언 and 선언.group(1) != Enw:
        raise SystemExit('Ffeil·공개 fformat_VALUE Enw 불일치: ' + str(LLWYBR))
print('UTF-8 공개 fformat_VALUE·Ffeil Enw dilysu 완료; 현지어 검토 상태는 국가판 명명 data cyfeiriad')
PY
