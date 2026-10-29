#!/bin/sh
set -eu
# 외국어판의 이름을 العربية 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for مسار in Path('قديم_مصدر').rglob('*.java'):
    اسم = مسار.stem
    if not اسم.isidentifier() or unicodedata.normalize('NFC', اسم) != اسم:
        raise SystemExit('معرف_قيمة 또는 يقلل_التكرار_قيمة خطأ: ' + str(مسار))
    مصدر = مسار.read_text(encoding='utf-8')
    إعلان = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', مصدر)
    if إعلان and إعلان.group(1) != اسم:
        raise SystemExit('ملف·공개 ينسق_قيمة اسم 불일치: ' + str(مسار))
print('UTF-8 공개 ينسق_قيمة·ملف اسم يتحقق 완료; 현지어 검토 상태는 국가판 명명 بيانات مرجع')
PY
