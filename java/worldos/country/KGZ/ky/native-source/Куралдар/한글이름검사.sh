#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for ЖОЛ in Path('мурасталган_башат').rglob('*.java'):
    Аты = ЖОЛ.stem
    if not Аты.isidentifier() or unicodedata.normalize('NFC', Аты) != Аты:
        raise SystemExit('аныктагыч_маани 또는 нормалдаштыруу_маани Ката: ' + str(ЖОЛ))
    Булак = ЖОЛ.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', Булак)
    if 선언 and 선언.group(1) != Аты:
        raise SystemExit('Файл·공개 формат_маани Аты 불일치: ' + str(ЖОЛ))
print('UTF-8 공개 формат_маани·Файл Аты тууралыгын_аныктоо 완료; 현지어 검토 상태는 국가판 명명 берилмелер Шилтемелер')
PY
