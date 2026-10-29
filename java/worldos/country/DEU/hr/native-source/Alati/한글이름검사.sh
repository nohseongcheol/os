#!/bin/sh
set -eu
# 외국어판의 이름을 hrvatski 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for PUTANJA in Path('nasljeđe_izvor').rglob('*.java'):
    Ime = PUTANJA.stem
    if not Ime.isidentifier() or unicodedata.normalize('NFC', Ime) != Ime:
        raise SystemExit('identifikator_VALUE 또는 normalizirati_VALUE GREŠKA: ' + str(PUTANJA))
    IZVOR = PUTANJA.read_text(encoding='utf-8')
    deklaracija = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', IZVOR)
    if deklaracija and deklaracija.group(1) != Ime:
        raise SystemExit('Datoteka·공개 oblik_VALUE Ime 불일치: ' + str(PUTANJA))
print('UTF-8 공개 oblik_VALUE·Datoteka Ime provjeriti 완료; 현지어 검토 상태는 국가판 명명 podaci Reference')
PY
