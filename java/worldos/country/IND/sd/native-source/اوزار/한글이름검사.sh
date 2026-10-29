#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for راههه in Path('ميراث_ماخذ').rglob('*.java'):
    نالو = راههه.stem
    if not نالو.isidentifier() or unicodedata.normalize('NFC', نالو) != نالو:
        raise SystemExit('سڃاڻپ_ڪندڙ_قدر 또는 عام_ڪرڻ_قدر نقص: ' + str(راههه))
    ماخذ = راههه.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ماخذ)
    if 선언 and 선언.group(1) != نالو:
        raise SystemExit('فائل·공개 وضع_قدر نالو 불일치: ' + str(راههه))
print('UTF-8 공개 وضع_قدر·فائل نالو تصديق_ڪريو 완료; 현지어 검토 상태는 국가판 명명 ڪوائف حوالو')
PY
