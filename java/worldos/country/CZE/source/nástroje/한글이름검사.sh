#!/bin/sh
set -eu
# 외국어판의 이름을 čeština 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for cesta_2 in Path('starší_verze_zdroj').rglob('*.java'):
    Název = cesta_2.stem
    if not Název.isidentifier() or unicodedata.normalize('NFC', Název) != Název:
        raise SystemExit('identifikátor_HODNOTA 또는 normalizovat_HODNOTA chyba: ' + str(cesta_2))
    zdrojový_soubor = cesta_2.read_text(encoding='utf-8')
    deklarace_4f4f026b = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', zdrojový_soubor)
    if deklarace_4f4f026b and deklarace_4f4f026b.group(1) != Název:
        raise SystemExit('název_souboru·공개 formát_HODNOTA Název 불일치: ' + str(cesta_2))
print('UTF-8 공개 formát_HODNOTA·název_souboru Název ověřit 완료; 현지어 검토 상태는 국가판 명명 data odkaz')
PY
