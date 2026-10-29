#!/bin/sh
set -eu
# 외국어판의 이름을 Română 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for Cale in Path('moștenit_sursă').rglob('*.java'):
    Nume = Cale.stem
    if not Nume.isidentifier() or unicodedata.normalize('NFC', Nume) != Nume:
        raise SystemExit('identificator_VALUE 또는 normaliza_VALUE eroare: ' + str(Cale))
    SURSĂ = Cale.read_text(encoding='utf-8')
    declarație = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', SURSĂ)
    if declarație and declarație.group(1) != Nume:
        raise SystemExit('Fișier·공개 format_VALUE Nume 불일치: ' + str(Cale))
print('UTF-8 공개 format_VALUE·Fișier Nume verifica 완료; 현지어 검토 상태는 국가판 명명 date referință')
PY
