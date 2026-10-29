#!/bin/sh
set -eu
# 외국어판의 이름을 isiXhosa 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for INDLELA in Path('eyayikhe_yenzeka_umthombo').rglob('*.java'):
    Igama = INDLELA.stem
    if not Igama.isidentifier() or unicodedata.normalize('NFC', Igama) != Igama:
        raise SystemExit('isalathisi_ixabiso 또는 qhelekisa_ixabiso Impazamo: ' + str(INDLELA))
    UMTHOMBO = INDLELA.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', UMTHOMBO)
    if 선언 and 선언.group(1) != Igama:
        raise SystemExit('iFayili·공개 fomatha_ixabiso Igama 불일치: ' + str(INDLELA))
print('UTF-8 공개 fomatha_ixabiso·iFayili Igama ngqinisisa 완료; 현지어 검토 상태는 국가판 명명 iingcombolo Isalathiso')
PY
