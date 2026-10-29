#!/bin/sh
set -eu
# 외국어판의 이름을 Slovenský 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for Cesta in Path('starší_zdroj').rglob('*.java'):
    Názov = Cesta.stem
    if not Názov.isidentifier() or unicodedata.normalize('NFC', Názov) != Názov:
        raise SystemExit('identifikátor_VALUE 또는 normalizovať_VALUE chyba: ' + str(Cesta))
    ZDROJ = Cesta.read_text(encoding='utf-8')
    deklarácia = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ZDROJ)
    if deklarácia and deklarácia.group(1) != Názov:
        raise SystemExit('Súbor·공개 formát_VALUE Názov 불일치: ' + str(Cesta))
print('UTF-8 공개 formát_VALUE·Súbor Názov overiť 완료; 현지어 검토 상태는 국가판 명명 údaje zdroj')
PY
