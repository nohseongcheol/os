#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for पाथ in Path('लिगसी_स्त्रोत').rglob('*.java'):
    नांव = पाथ.stem
    if not नांव.isidentifier() or unicodedata.normalize('NFC', नांव) != नांव:
        raise SystemExit('वळखुपी_मोल 또는 सामान्य_स्थितीर_येवचें_मोल चूक: ' + str(पाथ))
    स्त्रोत = पाथ.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', स्त्रोत)
    if 선언 and 선언.group(1) != नांव:
        raise SystemExit('फायल·공개 स्वरूप_मोल नांव 불일치: ' + str(पाथ))
print('UTF-8 공개 स्वरूप_मोल·फायल नांव पुनर्तपासणी_करची 완료; 현지어 검토 상태는 국가판 명명 डेटा संदर्भ')
PY
