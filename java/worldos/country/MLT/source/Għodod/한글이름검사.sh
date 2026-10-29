#!/bin/sh
set -eu
# 외국어판의 이름을 Malti 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for mogħdija in Path('legacy_sors').rglob('*.java'):
    isem = mogħdija.stem
    if not isem.isidentifier() or unicodedata.normalize('NFC', isem) != isem:
        raise SystemExit('identifikatur_VALUE 또는 nnormalizza_VALUE żball: ' + str(mogħdija))
    sors = mogħdija.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', sors)
    if 선언 and 선언.group(1) != isem:
        raise SystemExit('fajl·공개 format_VALUE isem 불일치: ' + str(mogħdija))
print('UTF-8 공개 format_VALUE·fajl isem vverifika 완료; 현지어 검토 상태는 국가판 명명 data Referenza')
PY
