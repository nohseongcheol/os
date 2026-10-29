#!/bin/sh
set -eu
# 외국어판의 이름을 русский 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for путь in Path('устаревший_источник').rglob('*.java'):
    Название = путь.stem
    if not Название.isidentifier() or unicodedata.normalize('NFC', Название) != Название:
        raise SystemExit('идентификатор_ЗНАЧЕН 또는 нормализовать_ЗНАЧЕН ошибка: ' + str(путь))
    исходныйКод = путь.read_text(encoding='utf-8')
    декларация = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', исходныйКод)
    if декларация and декларация.group(1) != Название:
        raise SystemExit('файл·공개 формат_ЗНАЧЕН Название 불일치: ' + str(путь))
print('UTF-8 공개 формат_ЗНАЧЕН·файл Название проверять 완료; 현지어 검토 상태는 국가판 명명 данные ссылка')
PY
