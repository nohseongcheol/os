#!/bin/sh
set -eu
# 외국어판의 이름을 Reo_Māori 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for ara in Path('tawhito_pūtake').rglob('*.java'):
    Ingoa = ara.stem
    if not Ingoa.isidentifier() or unicodedata.normalize('NFC', Ingoa) != Ingoa:
        raise SystemExit('pūtāutu_uara 또는 whakanoa_uara Pōhēhē: ' + str(ara))
    pūtake = ara.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', pūtake)
    if 선언 and 선언.group(1) != Ingoa:
        raise SystemExit('Kōnae·공개 hōputu_uara Ingoa 불일치: ' + str(ara))
print('UTF-8 공개 hōputu_uara·Kōnae Ingoa manatoko 완료; 현지어 검토 상태는 국가판 명명 raraunga Pūranga_kōrero')
PY
