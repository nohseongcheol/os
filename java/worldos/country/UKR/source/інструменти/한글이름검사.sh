#!/bin/sh
set -eu
# 외국어판의 이름을 українська 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for шлях in Path('застарілий_джерело').rglob('*.java'):
    Назва = шлях.stem
    if not Назва.isidentifier() or unicodedata.normalize('NFC', Назва) != Назва:
        raise SystemExit('ідентифікатор_значення 또는 нормалізувати_значення ПОМИЛКА: ' + str(шлях))
    вихіднийКод = шлях.read_text(encoding='utf-8')
    оголошення_4f4f026b = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', вихіднийКод)
    if оголошення_4f4f026b and оголошення_4f4f026b.group(1) != Назва:
        raise SystemExit('файл·공개 формат_значення Назва 불일치: ' + str(шлях))
print('UTF-8 공개 формат_значення·файл Назва перевіряти 완료; 현지어 검토 상태는 국가판 명명 дані довідка')
PY
