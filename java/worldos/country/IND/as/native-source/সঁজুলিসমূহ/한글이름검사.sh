#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for পথ in Path('লীগেছি_উৎস').rglob('*.java'):
    নাম = পথ.stem
    if not নাম.isidentifier() or unicodedata.normalize('NFC', নাম) != নাম:
        raise SystemExit('চিনাক্তকাৰী_মান 또는 সাধাৰণীকৰণ_কৰক_মান ত্ৰুটি: ' + str(পথ))
    উৎস = পথ.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', উৎস)
    if 선언 and 선언.group(1) != নাম:
        raise SystemExit('নথিপত্ৰ·공개 সজ্জা_মান নাম 불일치: ' + str(পথ))
print('UTF-8 공개 সজ্জা_মান·নথিপত্ৰ নাম প্ৰমাণিত_কৰক 완료; 현지어 검토 상태는 국가판 명명 ডাটা 참조')
PY
