#!/bin/sh
set -eu
# 외국어판의 이름을 norsk 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for Sti in Path('eldre_kilde').rglob('*.java'):
    Navn = Sti.stem
    if not Navn.isidentifier() or unicodedata.normalize('NFC', Navn) != Navn:
        raise SystemExit('identifikator_VERDI 또는 normalisere_VERDI feil: ' + str(Sti))
    KILDE = Sti.read_text(encoding='utf-8')
    erklæring = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', KILDE)
    if erklæring and erklæring.group(1) != Navn:
        raise SystemExit('Fil·공개 format_VERDI Navn 불일치: ' + str(Sti))
print('UTF-8 공개 format_VERDI·Fil Navn bekrefte 완료; 현지어 검토 상태는 국가판 명명 data referere')
PY
