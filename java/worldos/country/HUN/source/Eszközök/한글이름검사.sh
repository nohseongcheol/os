#!/bin/sh
set -eu
# 외국어판의 이름을 magyar 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for ÚTVONAL in Path('örökség_forrás').rglob('*.java'):
    Név = ÚTVONAL.stem
    if not Név.isidentifier() or unicodedata.normalize('NFC', Név) != Név:
        raise SystemExit('azonosító_ÉRTÉK 또는 normalizál_ÉRTÉK HIBA: ' + str(ÚTVONAL))
    FORRÁS = ÚTVONAL.read_text(encoding='utf-8')
    bevallás = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', FORRÁS)
    if bevallás and bevallás.group(1) != Név:
        raise SystemExit('Fájl·공개 formáz_ÉRTÉK Név 불일치: ' + str(ÚTVONAL))
print('UTF-8 공개 formáz_ÉRTÉK·Fájl Név igazol 완료; 현지어 검토 상태는 국가판 명명 adat hivatkozik')
PY
