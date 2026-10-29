#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for Tsejana in Path('ya_kgale_mohlodi').rglob('*.java'):
    Leina = Tsejana.stem
    if not Leina.isidentifier() or unicodedata.normalize('NFC', Leina) != Leina:
        raise SystemExit('sešupi_boleng 또는 fokotša_kopišo_boleng Phošo: ' + str(Tsejana))
    mohlodi = Tsejana.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', mohlodi)
    if 선언 and 선언.group(1) != Leina:
        raise SystemExit('Faele·공개 fomete_boleng Leina 불일치: ' + str(Tsejana))
print('UTF-8 공개 fomete_boleng·Faele Leina kgonthiša 완료; 현지어 검토 상태는 국가판 명명 data Dipadišo')
PY
