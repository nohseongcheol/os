#!/bin/sh
set -eu
# 외국어판의 이름을 Ikinyarwanda 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for Inzira in Path('umurage_inkomoko').rglob('*.java'):
    Izina = Inzira.stem
    if not Izina.isidentifier() or unicodedata.normalize('NFC', Izina) != Izina:
        raise SystemExit('indanga_agaciro 또는 kuboneza_agaciro IKOSA: ' + str(Inzira))
    Inkomoko = Inzira.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', Inkomoko)
    if 선언 and 선언.group(1) != Izina:
        raise SystemExit('Idosiye·공개 imiterere_agaciro Izina 불일치: ' + str(Inzira))
print('UTF-8 공개 imiterere_agaciro·Idosiye Izina gusuzuma 완료; 현지어 검토 상태는 국가판 명명 amakurushingiro Indanga')
PY
