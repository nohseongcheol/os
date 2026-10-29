#!/bin/sh
set -eu
# 외국어판의 이름을 Svenska 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for sökväg_2 in Path('äldre_källa').rglob('*.java'):
    Namn = sökväg_2.stem
    if not Namn.isidentifier() or unicodedata.normalize('NFC', Namn) != Namn:
        raise SystemExit('identifierare_värde 또는 normalisera_värde fel: ' + str(sökväg_2))
    källfil = sökväg_2.read_text(encoding='utf-8')
    deklaration = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', källfil)
    if deklaration and deklaration.group(1) != Namn:
        raise SystemExit('filnamn·공개 format_värde Namn 불일치: ' + str(sökväg_2))
print('UTF-8 공개 format_värde·filnamn Namn verifiera 완료; 현지어 검토 상태는 국가판 명명 data referens')
PY
