#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for Putanja in Path('naslijeđe_izvor').rglob('*.java'):
    Naziv = Putanja.stem
    if not Naziv.isidentifier() or unicodedata.normalize('NFC', Naziv) != Naziv:
        raise SystemExit('identifikator_VALUE 또는 normalizirati_VALUE GRESKA: ' + str(Putanja))
    IZVOR = Putanja.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', IZVOR)
    if 선언 and 선언.group(1) != Naziv:
        raise SystemExit('Fajl·공개 format_VALUE Naziv 불일치: ' + str(Putanja))
print('UTF-8 공개 format_VALUE·Fajl Naziv potvrditi 완료; 현지어 검토 상태는 국가판 명명 podaci Reference')
PY
