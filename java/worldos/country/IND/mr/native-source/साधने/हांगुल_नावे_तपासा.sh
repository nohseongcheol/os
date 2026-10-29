#!/bin/sh
set -eu
# 외국어판의 이름을 मराठी 전용 규칙으로 거부하지 않는다.
# अर्थ_मूल्य·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for मार्ग in Path('लेगसी_स्रोत').rglob('*.java'):
    नाव = मार्ग.stem
    if not नाव.isidentifier() or unicodedata.normalize('NFC', नाव) != नाव:
        raise SystemExit('आयडेंटिफायर_मूल्य 또는 सामान्यीकरण_करा_मूल्य त्रुटी: ' + str(मार्ग))
    स्रोत = मार्ग.read_text(encoding='utf-8')
    घोषणा = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', स्रोत)
    if घोषणा and घोषणा.group(1) != नाव:
        raise SystemExit('फाइल·공개 स्वरूप_मूल्य नाव 불일치: ' + str(मार्ग))
print('UTF-8 공개 स्वरूप_मूल्य·फाइल नाव पडताळा आहे_पूर्ण; 현지어 검토 상태는 국가판 नामकरण डेटा संदर्भ')
PY
