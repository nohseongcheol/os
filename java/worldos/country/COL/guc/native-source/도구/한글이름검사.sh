#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for wopu_a_ttaaleemüin in Path('apaaluushi_eejeejetülein').rglob('*.java'):
    이름 = wopu_a_ttaaleemüin.stem
    if not 이름.isidentifier() or unicodedata.normalize('NFC', 이름) != 이름:
        raise SystemExit('식별자 또는 anaajaa_ajutuu ajachitia: ' + str(wopu_a_ttaaleemüin))
    eejeejetülein = wopu_a_ttaaleemüin.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', eejeejetülein)
    if 선언 and 선언.group(1) != 이름:
        raise SystemExit('anaajaalaa·공개 akua_ipaa_ajutuu 이름 불일치: ' + str(wopu_a_ttaaleemüin))
print('UTF-8 공개 akua_ipaa_ajutuu·anaajaalaa 이름 확인 완료; 현지어 검토 상태는 국가판 명명 atijaaya 참조')
PY
