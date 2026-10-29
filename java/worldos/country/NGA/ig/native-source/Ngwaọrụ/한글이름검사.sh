#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for ụzọ_ozi in Path('ekpe_ebensìbịa').rglob('*.java'):
    Aha = ụzọ_ozi.stem
    if not Aha.isidentifier() or unicodedata.normalize('NFC', Aha) != Aha:
        raise SystemExit('ihe_nkọwapụta_valuu 또는 mèzima_valuu mmejọ: ' + str(ụzọ_ozi))
    ebensìbịa = ụzọ_ozi.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ebensìbịa)
    if 선언 and 선언.group(1) != Aha:
        raise SystemExit('Faịlụ·공개 hàzie_valuu Aha 불일치: ' + str(ụzọ_ozi))
print('UTF-8 공개 hàzie_valuu·Faịlụ Aha nkwàdo_eziokwū 완료; 현지어 검토 상태는 국가판 명명 datà Nrụtụ_aka')
PY
