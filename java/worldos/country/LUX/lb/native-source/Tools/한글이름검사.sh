#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for Wee in Path('al_Quell').rglob('*.java'):
    Numm = Wee.stem
    if not Numm.isidentifier() or unicodedata.normalize('NFC', Numm) != Numm:
        raise SystemExit('Identifikateur_VALUE 또는 normaliséieren_VALUE Feeler: ' + str(Wee))
    Quell = Wee.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', Quell)
    if 선언 and 선언.group(1) != Numm:
        raise SystemExit('Fichier·공개 Format_VALUE Numm 불일치: ' + str(Wee))
print('UTF-8 공개 Format_VALUE·Fichier Numm verifizéieren 완료; 현지어 검토 상태는 국가판 명명 Daten Referenzen')
PY
