#!/bin/sh
set -eu
# 외국어판의 이름을 Eesti 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for RADA in Path('pärand_lähe').rglob('*.java'):
    Nimi_2 = RADA.stem
    if not Nimi_2.isidentifier() or unicodedata.normalize('NFC', Nimi_2) != Nimi_2:
        raise SystemExit('identifikaator_VALUE 또는 normaliseerima_VALUE VIGA: ' + str(RADA))
    ALLIKAS = RADA.read_text(encoding='utf-8')
    deklaratsioon = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ALLIKAS)
    if deklaratsioon and deklaratsioon.group(1) != Nimi_2:
        raise SystemExit('Fail·공개 vorming_VALUE Nimi_2 불일치: ' + str(RADA))
print('UTF-8 공개 vorming_VALUE·Fail Nimi_2 kinnitama 완료; 현지어 검토 상태는 국가판 명명 andmed viide')
PY
