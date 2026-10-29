#!/bin/sh
set -eu
# 외국어판의 이름을 বাংলা 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for পথ_2 in Path('ঐতিহ্য_উত্স').rglob('*.java'):
    নাম = পথ_2.stem
    if not নাম.isidentifier() or unicodedata.normalize('NFC', নাম) != নাম:
        raise SystemExit('সনাক্তকারী_মান 또는 সাধারণকরণ_মান ত্রুটি: ' + str(পথ_2))
    উৎস_নথি = পথ_2.read_text(encoding='utf-8')
    ঘোষণা = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', উৎস_নথি)
    if ঘোষণা and ঘোষণা.group(1) != নাম:
        raise SystemExit('নথির_নাম·공개 বিন্যাস_মান নাম 불일치: ' + str(পথ_2))
print('UTF-8 공개 বিন্যাস_মান·নথির_নাম নাম যাচাই_করা 완료; 현지어 검토 상태는 국가판 명명 ডাটা প্রসঙ্গ')
PY
