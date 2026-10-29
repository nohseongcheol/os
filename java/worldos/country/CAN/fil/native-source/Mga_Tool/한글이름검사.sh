#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for path in Path('pamana_pinagmulan').rglob('*.java'):
    pangalan = path.stem
    if not pangalan.isidentifier() or unicodedata.normalize('NFC', pangalan) != pangalan:
        raise SystemExit('tagakilala_VALUE 또는 normalisahin_VALUE error: ' + str(path))
    pinagmulan = path.read_text(encoding='utf-8')
    declaration = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', pinagmulan)
    if declaration and declaration.group(1) != pangalan:
        raise SystemExit('file·공개 format_VALUE pangalan 불일치: ' + str(path))
print('UTF-8 공개 format_VALUE·file pangalan tiyakin_kumpirmahin 완료; 현지어 검토 상태는 국가판 명명 data Sanggunian')
PY
