#!/bin/sh
set -eu
# 외국어판의 이름을 עברית 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for נתיב in Path('דור_קודם_מקור').rglob('*.java'):
    שם = נתיב.stem
    if not שם.isidentifier() or unicodedata.normalize('NFC', שם) != שם:
        raise SystemExit('מזהה_ערך 또는 לנרמל_ערך שגיאה: ' + str(נתיב))
    קודמקור = נתיב.read_text(encoding='utf-8')
    הצהרה = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', קודמקור)
    if הצהרה and הצהרה.group(1) != שם:
        raise SystemExit('קובץ·공개 לעצב_ערך שם 불일치: ' + str(נתיב))
print('UTF-8 공개 לעצב_ערך·קובץ שם ודא_אמת 완료; 현지어 검토 상태는 국가판 명명 נתונים הפנה')
PY
