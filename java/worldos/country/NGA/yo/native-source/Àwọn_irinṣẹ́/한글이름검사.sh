#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for ọ̀nà in Path('tàtijọ́_orísun').rglob('*.java'):
    Orúkọ = ọ̀nà.stem
    if not Orúkọ.isidentifier() or unicodedata.normalize('NFC', Orúkọ) != Orúkọ:
        raise SystemExit('Àfidámọ̀_iye 또는 ṣe_níwọ̀n_iye àṣìṣe: ' + str(ọ̀nà))
    orísun = ọ̀nà.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', orísun)
    if 선언 and 선언.group(1) != Orúkọ:
        raise SystemExit('Fáìlì·공개 ìgúnrégé_iye Orúkọ 불일치: ' + str(ọ̀nà))
print('UTF-8 공개 ìgúnrégé_iye·Fáìlì Orúkọ ridájú 완료; 현지어 검토 상태는 국가판 명명 détà Ìtọ́ka')
PY
