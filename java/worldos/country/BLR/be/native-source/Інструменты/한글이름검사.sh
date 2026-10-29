#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for ШЛЯХ in Path('ранейшых_версій_крыніца').rglob('*.java'):
    Назва = ШЛЯХ.stem
    if not Назва.isidentifier() or unicodedata.normalize('NFC', Назва) != Назва:
        raise SystemExit('ідэнтыфікатар_значэнне 또는 нармалізаваць_значэнне ПАМЫЛКА: ' + str(ШЛЯХ))
    КРЫНІЦА = ШЛЯХ.read_text(encoding='utf-8')
    абвяшчэнне = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', КРЫНІЦА)
    if абвяшчэнне and абвяшчэнне.group(1) != Назва:
        raise SystemExit('Файл·공개 фармат_значэнне Назва 불일치: ' + str(ШЛЯХ))
print('UTF-8 공개 фармат_значэнне·Файл Назва праверыць 완료; 현지어 검토 상태는 국가판 명명 дадзеныя Даведачныя_матэрыялы')
PY
