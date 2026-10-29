#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for масир in Path('ирсӣ_манбаъ').rglob('*.java'):
    Ном = масир.stem
    if not Ном.isidentifier() or unicodedata.normalize('NFC', Ном) != Ном:
        raise SystemExit('идентификатор_қимат 또는 ба_тартиб_даровардан_қимат Хато: ' + str(масир))
    манбаъ = масир.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', манбаъ)
    if 선언 and 선언.group(1) != Ном:
        raise SystemExit('Файл·공개 формат_қимат Ном 불일치: ' + str(масир))
print('UTF-8 공개 формат_қимат·Файл Ном тасдиқ_кардан 완료; 현지어 검토 상태는 국가판 명명 иттилоот Маълумотнома')
PY
