#!/bin/sh
set -eu
# 외국어판의 이름을 ગુજરાતી 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for પથ in Path('લેગસી_સ્રોત').rglob('*.java'):
    નામ = પથ.stem
    if not નામ.isidentifier() or unicodedata.normalize('NFC', નામ) != નામ:
        raise SystemExit('ઓળખકર્તા_મૂલ્ય 또는 સામાન્ય_બનાવો_મૂલ્ય ભૂલ: ' + str(પથ))
    સ્રોત = પથ.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', સ્રોત)
    if 선언 and 선언.group(1) != નામ:
        raise SystemExit('ફાઈલ·공개 સ્વરૂપ_મૂલ્ય નામ 불일치: ' + str(પથ))
print('UTF-8 공개 સ્વરૂપ_મૂલ્ય·ફાઈલ નામ ચકાસવું 완료; 현지어 검토 상태는 국가판 명명 ડેટા સંદર્ભ')
PY
