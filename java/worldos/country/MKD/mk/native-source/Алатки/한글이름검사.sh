#!/bin/sh
set -eu
# 외국어판의 이름을 Македонски 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for ПАТЕКА in Path('наследен_извор').rglob('*.java'):
    Име = ПАТЕКА.stem
    if not Име.isidentifier() or unicodedata.normalize('NFC', Име) != Име:
        raise SystemExit('идентификатор_VALUE 또는 нормализирање_VALUE ГРЕШКА: ' + str(ПАТЕКА))
    ИЗВОР = ПАТЕКА.read_text(encoding='utf-8')
    декларација = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ИЗВОР)
    if декларација and декларација.group(1) != Име:
        raise SystemExit('Датотека·공개 формат_VALUE Име 불일치: ' + str(ПАТЕКА))
print('UTF-8 공개 формат_VALUE·Датотека Име провери 완료; 현지어 검토 상태는 국가판 명명 податоци Референци')
PY
