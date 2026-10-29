#!/bin/sh
set -eu
# 외국어판의 이름을 Italiano 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for percorso in Path('legacy_fonte').rglob('*.java'):
    Nome = percorso.stem
    if not Nome.isidentifier() or unicodedata.normalize('NFC', Nome) != Nome:
        raise SystemExit('identificatore_VALORE 또는 normalizzare_VALORE errore: ' + str(percorso))
    codiceSorgente = percorso.read_text(encoding='utf-8')
    dichiarazione = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', codiceSorgente)
    if dichiarazione and dichiarazione.group(1) != Nome:
        raise SystemExit('file·공개 formato_VALORE Nome 불일치: ' + str(percorso))
print('UTF-8 공개 formato_VALORE·file Nome verificare 완료; 현지어 검토 상태는 국가판 명명 dati fonti')
PY
