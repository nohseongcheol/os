#!/bin/sh
set -eu
# 외국어판의 이름을 Latviešu 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for CEĻŠ in Path('mantots_avots').rglob('*.java'):
    Nosaukums = CEĻŠ.stem
    if not Nosaukums.isidentifier() or unicodedata.normalize('NFC', Nosaukums) != Nosaukums:
        raise SystemExit('identifikators_VALUE 또는 normalizēt_VALUE Kļūda: ' + str(CEĻŠ))
    AVOTS = CEĻŠ.read_text(encoding='utf-8')
    deklarācija = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', AVOTS)
    if deklarācija and deklarācija.group(1) != Nosaukums:
        raise SystemExit('Fails·공개 formāts_VALUE Nosaukums 불일치: ' + str(CEĻŠ))
print('UTF-8 공개 formāts_VALUE·Fails Nosaukums verificēt 완료; 현지어 검토 상태는 국가판 명명 dati Uzziņas')
PY
