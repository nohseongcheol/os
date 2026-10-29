#!/bin/sh
set -eu
# 외국어판의 이름을 Nederlands 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for pad in Path('verouderd_bron').rglob('*.java'):
    Naam = pad.stem
    if not Naam.isidentifier() or unicodedata.normalize('NFC', Naam) != Naam:
        raise SystemExit('id_WAARDE 또는 normaliseren_WAARDE fout: ' + str(pad))
    broncode = pad.read_text(encoding='utf-8')
    aangifte = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', broncode)
    if aangifte and aangifte.group(1) != Naam:
        raise SystemExit('bestand·공개 opmaak_WAARDE Naam 불일치: ' + str(pad))
print('UTF-8 공개 opmaak_WAARDE·bestand Naam bevestigen 완료; 현지어 검토 상태는 국가판 명명 gegevens verwijzen')
PY
