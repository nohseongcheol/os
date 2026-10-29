#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for Pad in Path('reedsbestaande_bron').rglob('*.java'):
    Naam = Pad.stem
    if not Naam.isidentifier() or unicodedata.normalize('NFC', Naam) != Naam:
        raise SystemExit('waarde_VALUE 또는 normaliseer_VALUE Fout: ' + str(Pad))
    Bron = Pad.read_text(encoding='utf-8')
    verklaring = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', Bron)
    if verklaring and verklaring.group(1) != Naam:
        raise SystemExit('Lêer·공개 formaat_VALUE Naam 불일치: ' + str(Pad))
print('UTF-8 공개 formaat_VALUE·Lêer Naam verifieer 완료; 현지어 검토 상태는 국가판 명명 data Naslaan')
PY
