#!/bin/sh
set -eu
# 외국어판의 이름을 नेपाली 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for मार्ग in Path('बिरासत_स्रोत').rglob('*.java'):
    नाम = मार्ग.stem
    if not नाम.isidentifier() or unicodedata.normalize('NFC', नाम) != नाम:
        raise SystemExit('परिचायक_मान 또는 सामान्यकरण_गर्नुहोस्_मान त्रुटि: ' + str(मार्ग))
    स्रोत = मार्ग.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', स्रोत)
    if 선언 and 선언.group(1) != नाम:
        raise SystemExit('फाइल·공개 ढाँचा_मान नाम 불일치: ' + str(मार्ग))
print('UTF-8 공개 ढाँचा_मान·फाइल नाम रुजू_गर्नुहोस् 완료; 현지어 검토 상태는 국가판 명명 लगत निर्देश')
PY
