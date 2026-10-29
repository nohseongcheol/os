#!/bin/sh
set -eu
# 외국어판의 이름을 Euskara 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for Bide_izena in Path('legatu_iturburu').rglob('*.java'):
    Izena = Bide_izena.stem
    if not Izena.isidentifier() or unicodedata.normalize('NFC', Izena) != Izena:
        raise SystemExit('identifikatzaile_balio 또는 normalizatu_balio errorea: ' + str(Bide_izena))
    ITURBURUA = Bide_izena.read_text(encoding='utf-8')
    deklarazio = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ITURBURUA)
    if deklarazio and deklarazio.group(1) != Izena:
        raise SystemExit('Fitxategia·공개 formatu_balio Izena 불일치: ' + str(Bide_izena))
print('UTF-8 공개 formatu_balio·Fitxategia Izena egiaztatu 완료; 현지어 검토 상태는 국가판 명명 datuak Erreferentzia_materiala')
PY
