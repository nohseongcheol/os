#!/bin/sh
set -eu
# 외국어판의 이름을 English 전용 규칙으로 거부하지 않는다.
# meaningValue·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for path in Path('legacySource').rglob('*.java'):
    name = path.stem
    if not name.isidentifier() or unicodedata.normalize('NFC', name) != name:
        raise SystemExit('identifierValue 또는 normalizeValue error: ' + str(path))
    source = path.read_text(encoding='utf-8')
    Declaration = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', source)
    if Declaration and Declaration.group(1) != name:
        raise SystemExit('file·공개 formatValue name 불일치: ' + str(path))
print('UTF-8 공개 formatValue·file name verify isComplete; 현지어 검토 상태는 국가판 naming data reference')
PY
