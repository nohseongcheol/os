#!/bin/sh
set -eu
# 외국어판의 이름을 Lietuvių 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for KELIAS in Path('senstelėjusi_įranga_šaltinis').rglob('*.java'):
    Pavadinimas_2 = KELIAS.stem
    if not Pavadinimas_2.isidentifier() or unicodedata.normalize('NFC', Pavadinimas_2) != Pavadinimas_2:
        raise SystemExit('identifikatorius_VALUE 또는 normalizuoti_VALUE KLAIDA: ' + str(KELIAS))
    ŠALTINIS = KELIAS.read_text(encoding='utf-8')
    deklaracija = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ŠALTINIS)
    if deklaracija and deklaracija.group(1) != Pavadinimas_2:
        raise SystemExit('Failas·공개 formatas_VALUE Pavadinimas_2 불일치: ' + str(KELIAS))
print('UTF-8 공개 formatas_VALUE·Failas Pavadinimas_2 patvirtinti 완료; 현지어 검토 상태는 국가판 명명 duomenys nuoroda')
PY
