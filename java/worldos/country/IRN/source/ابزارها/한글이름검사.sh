#!/bin/sh
set -eu
# 외국어판의 이름을 فارسی 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for مسیر in Path('موروثی_منبع').rglob('*.java'):
    نام = مسیر.stem
    if not نام.isidentifier() or unicodedata.normalize('NFC', نام) != نام:
        raise SystemExit('شناسه_مقدار 또는 بهنجار_کردن_مقدار خطا: ' + str(مسیر))
    مبداء = مسیر.read_text(encoding='utf-8')
    اعلامیه = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', مبداء)
    if اعلامیه and اعلامیه.group(1) != نام:
        raise SystemExit('پرونده·공개 قالب_مقدار نام 불일치: ' + str(مسیر))
print('UTF-8 공개 قالب_مقدار·پرونده نام تأیید_صحت 완료; 현지어 검토 상태는 국가판 명명 داده_ها مرجع')
PY
