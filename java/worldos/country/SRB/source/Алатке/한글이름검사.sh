#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for ПУТАЊА in Path('наслијеђе_извор').rglob('*.java'):
    Назив = ПУТАЊА.stem
    if not Назив.isidentifier() or unicodedata.normalize('NFC', Назив) != Назив:
        raise SystemExit('идентификатор_вриједност 또는 нормализовати_вриједност ГРЕШКА: ' + str(ПУТАЊА))
    ИЗВОР = ПУТАЊА.read_text(encoding='utf-8')
    декларација = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ИЗВОР)
    if декларација and декларација.group(1) != Назив:
        raise SystemExit('Датотека·공개 формат_вриједност Назив 불일치: ' + str(ПУТАЊА))
print('UTF-8 공개 формат_вриједност·Датотека Назив потврдити 완료; 현지어 검토 상태는 국가판 명명 подаци Литература')
PY
