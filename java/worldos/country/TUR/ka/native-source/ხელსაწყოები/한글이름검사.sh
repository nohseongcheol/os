#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for გეზი in Path('მოძველებული_წყარო').rglob('*.java'):
    სახელი = გეზი.stem
    if not სახელი.isidentifier() or unicodedata.normalize('NFC', სახელი) != სახელი:
        raise SystemExit('იდენტიფიკატორი_მნიშვნელობა 또는 მოწესრიგება_მნიშვნელობა შეცდომა: ' + str(გეზი))
    წყარო = გეზი.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', წყარო)
    if 선언 and 선언.group(1) != სახელი:
        raise SystemExit('ფაილი·공개 ფორმატი_მნიშვნელობა სახელი 불일치: ' + str(გეზი))
print('UTF-8 공개 ფორმატი_მნიშვნელობა·ფაილი სახელი გადამოწმება 완료; 현지어 검토 상태는 국가판 명명 მონაცემები ცნობარები')
PY
