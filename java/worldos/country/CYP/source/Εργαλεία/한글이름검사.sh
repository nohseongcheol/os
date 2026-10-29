#!/bin/sh
set -eu
# 외국어판의 이름을 ελληνικά 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for ΔΙΑΔΡΟΜΗ in Path('παλαιού_τύπου_προέλευση').rglob('*.java'):
    Όνομα = ΔΙΑΔΡΟΜΗ.stem
    if not Όνομα.isidentifier() or unicodedata.normalize('NFC', Όνομα) != Όνομα:
        raise SystemExit('αναγνωριστικό_τιμή 또는 κανονικοποίηση_τιμή ΣΦΑΛΜΑ: ' + str(ΔΙΑΔΡΟΜΗ))
    ΠΗΓΗ = ΔΙΑΔΡΟΜΗ.read_text(encoding='utf-8')
    δήλωση = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ΠΗΓΗ)
    if δήλωση and δήλωση.group(1) != Όνομα:
        raise SystemExit('Αρχείο·공개 μορφή_τιμή Όνομα 불일치: ' + str(ΔΙΑΔΡΟΜΗ))
print('UTF-8 공개 μορφή_τιμή·Αρχείο Όνομα επαληθεύω 완료; 현지어 검토 상태는 국가판 명명 δεδομένα Αναφορά')
PY
