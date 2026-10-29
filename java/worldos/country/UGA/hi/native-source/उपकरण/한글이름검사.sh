#!/bin/sh
set -eu
# 외국어판의 이름을 हिंदी 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for पथ in Path('लिगेसी_स्रोत').rglob('*.java'):
    नाम = पथ.stem
    if not नाम.isidentifier() or unicodedata.normalize('NFC', नाम) != नाम:
        raise SystemExit('पहचानकर्ता_मान 또는 सामान्य_करें_मान त्रुटि: ' + str(पथ))
    स्रोत = पथ.read_text(encoding='utf-8')
    घोषणा = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', स्रोत)
    if घोषणा and घोषणा.group(1) != नाम:
        raise SystemExit('संचिका·공개 फॉर्मैट_मान नाम 불일치: ' + str(पथ))
print('UTF-8 공개 फॉर्मैट_मान·संचिका नाम सत्यापित_करें 완료; 현지어 검토 상태는 국가판 명명 आँकड़े संदर्भ')
PY
