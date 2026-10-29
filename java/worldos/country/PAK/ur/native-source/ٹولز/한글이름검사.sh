#!/bin/sh
set -eu
# 외국어판의 이름을 اردو 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for راستہ_2 in Path('ورثہ_ماخذ').rglob('*.java'):
    نام = راستہ_2.stem
    if not نام.isidentifier() or unicodedata.normalize('NFC', نام) != نام:
        raise SystemExit('شناخت_کنندہ_قدر 또는 عمومی_بنائيں_قدر غلطی: ' + str(راستہ_2))
    ماخذ_فائل = راستہ_2.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ماخذ_فائل)
    if 선언 and 선언.group(1) != نام:
        raise SystemExit('فائل_کا_نام·공개 وضع_قدر نام 불일치: ' + str(راستہ_2))
print('UTF-8 공개 وضع_قدر·فائل_کا_نام نام تصدیق_کریں 완료; 현지어 검토 상태는 국가판 명명 کوائف حوالہ_جات')
PY
