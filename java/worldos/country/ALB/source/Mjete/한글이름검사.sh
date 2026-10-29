#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for POZICIONI in Path('trashëgim_burim').rglob('*.java'):
    Emër = POZICIONI.stem
    if not Emër.isidentifier() or unicodedata.normalize('NFC', Emër) != Emër:
        raise SystemExit('identifikues_VALUE 또는 normalizoj_VALUE GABIM: ' + str(POZICIONI))
    BURIMI = POZICIONI.read_text(encoding='utf-8')
    deklarata = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', BURIMI)
    if deklarata and deklarata.group(1) != Emër:
        raise SystemExit('Kartelë·공개 format_VALUE Emër 불일치: ' + str(POZICIONI))
print('UTF-8 공개 format_VALUE·Kartelë Emër verifikoj 완료; 현지어 검토 상태는 국가판 명명 të_dhëna Referencë')
PY
