#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for Slighe in Path('oighreachd_tùs').rglob('*.java'):
    Ainm = Slighe.stem
    if not Ainm.isidentifier() or unicodedata.normalize('NFC', Ainm) != Ainm:
        raise SystemExit('aithnichear_VALUE 또는 àbhaistich_VALUE Mearachd: ' + str(Slighe))
    tùs = Slighe.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', tùs)
    if 선언 and 선언.group(1) != Ainm:
        raise SystemExit('faidhle·공개 fòrmat_VALUE Ainm 불일치: ' + str(Slighe))
print('UTF-8 공개 fòrmat_VALUE·faidhle Ainm dearbh 완료; 현지어 검토 상태는 국가판 명명 dàta fiosrachadh')
PY
