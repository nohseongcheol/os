#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for STIGE in Path('eldre_kjelde').rglob('*.java'):
    Namn = STIGE.stem
    if not Namn.isidentifier() or unicodedata.normalize('NFC', Namn) != Namn:
        raise SystemExit('identifikator_VALUE 또는 normalisere_VALUE FEIL: ' + str(STIGE))
    KJELDE = STIGE.read_text(encoding='utf-8')
    erklæring = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', KJELDE)
    if erklæring and erklæring.group(1) != Namn:
        raise SystemExit('Fil·공개 format_VALUE Namn 불일치: ' + str(STIGE))
print('UTF-8 공개 format_VALUE·Fil Namn stadfeste 완료; 현지어 검토 상태는 국가판 명명 data Oppslagsverk')
PY
