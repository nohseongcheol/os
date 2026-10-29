#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for گوزەر in Path('جێماو_ژێدەر').rglob('*.java'):
    ناو = گوزەر.stem
    if not ناو.isidentifier() or unicodedata.normalize('NFC', ناو) != ناو:
        raise SystemExit('ناسێنەر_نرخ 또는 ئاساییکردن_نرخ هەڵە: ' + str(گوزەر))
    ژێدەر = گوزەر.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ژێدەر)
    if 선언 and 선언.group(1) != ناو:
        raise SystemExit('فایل·공개 بیچم_نرخ ناو 불일치: ' + str(گوزەر))
print('UTF-8 공개 بیچم_نرخ·فایل ناو سەلماندن 완료; 현지어 검토 상태는 국가판 명명 دەیتا سەرچاوە')
PY
