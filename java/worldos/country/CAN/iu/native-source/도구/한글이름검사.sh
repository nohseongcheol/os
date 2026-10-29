#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for aqqut in Path('pituqaq_pivviujuq').rglob('*.java'):
    atiq = aqqut.stem
    if not atiq.isidentifier() or unicodedata.normalize('NFC', atiq) != atiq:
        raise SystemExit('식별자 또는 naammasitilli_atuutilik tammarniq: ' + str(aqqut))
    pivviujuq = aqqut.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', pivviujuq)
    if 선언 and 선언.group(1) != atiq:
        raise SystemExit('ini·공개 aaqqisurli_atuutilik atiq 불일치: ' + str(aqqut))
print('UTF-8 공개 aaqqisurli_atuutilik·ini atiq nalunairli_1aacb54c 완료; 현지어 검토 상태는 국가판 명명 titiqqat 참조')
PY
