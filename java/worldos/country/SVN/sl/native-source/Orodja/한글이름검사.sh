#!/bin/sh
set -eu
# 외국어판의 이름을 slovenščina 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for POT in Path('starejši_vir').rglob('*.java'):
    Ime = POT.stem
    if not Ime.isidentifier() or unicodedata.normalize('NFC', Ime) != Ime:
        raise SystemExit('identifikator_VALUE 또는 normalizirati_VALUE NAPAKA: ' + str(POT))
    VIR = POT.read_text(encoding='utf-8')
    deklaracija = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', VIR)
    if deklaracija and deklaracija.group(1) != Ime:
        raise SystemExit('Datoteka·공개 oblika_VALUE Ime 불일치: ' + str(POT))
print('UTF-8 공개 oblika_VALUE·Datoteka Ime 확인 완료; 현지어 검토 상태는 국가판 명명 podatki Gradiva')
PY
