#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for putanja in Path('zastareo_izvor').rglob('*.java'):
    ime = putanja.stem
    if not ime.isidentifier() or unicodedata.normalize('NFC', ime) != ime:
        raise SystemExit('identifikator_VALUE 또는 normalizovati_VALUE greška: ' + str(putanja))
    izvor = putanja.read_text(encoding='utf-8')
    deklaracija = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', izvor)
    if deklaracija and deklaracija.group(1) != ime:
        raise SystemExit('Datoteka·공개 format_VALUE ime 불일치: ' + str(putanja))
print('UTF-8 공개 format_VALUE·Datoteka ime verifikovati 완료; 현지어 검토 상태는 국가판 명명 podaci referenca')
PY
