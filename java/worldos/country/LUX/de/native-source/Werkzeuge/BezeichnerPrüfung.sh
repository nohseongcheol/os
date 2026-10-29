#!/bin/sh
set -eu
# 외국어판의 이름을 Deutsch 전용 규칙으로 거부하지 않는다.
# bedeutungWert·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for pfad in Path('Kernquelltext').rglob('*.java'):
    Name = pfad.stem
    if not Name.isidentifier() or unicodedata.normalize('NFC', Name) != Name:
        raise SystemExit('bezeichnerWert 또는 wertNormalisieren fehler: ' + str(pfad))
    Quelltext = pfad.read_text(encoding='utf-8')
    Deklarationen = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', Quelltext)
    if Deklarationen and Deklarationen.group(1) != Name:
        raise SystemExit('Datei·공개 formatWert Name 불일치: ' + str(pfad))
print('UTF-8 공개 formatWert·Datei Name überprüfen istFertig; 현지어 검토 상태는 국가판 benennung Daten verweis')
PY
