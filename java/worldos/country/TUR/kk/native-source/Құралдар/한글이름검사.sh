#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for Жол_2 in Path('бұрынғы_көз').rglob('*.java'):
    Аты = Жол_2.stem
    if not Аты.isidentifier() or unicodedata.normalize('NFC', Аты) != Аты:
        raise SystemExit('идентификатор_мән 또는 нормалдау_мән Қате: ' + str(Жол_2))
    Неден = Жол_2.read_text(encoding='utf-8')
    мәлімдеме = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', Неден)
    if мәлімдеме and мәлімдеме.group(1) != Аты:
        raise SystemExit('Файл·공개 пішім_мән Аты 불일치: ' + str(Жол_2))
print('UTF-8 공개 пішім_мән·Файл Аты тексеру 완료; 현지어 검토 상태는 국가판 명명 деректер Анықтамалық')
PY
