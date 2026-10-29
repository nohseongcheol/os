#!/bin/sh
set -eu
# 외국어판의 이름을 አማርኛ 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for መተላለፊያ in Path('ነባር_ምንጭ').rglob('*.java'):
    ስም = መተላለፊያ.stem
    if not ስም.isidentifier() or unicodedata.normalize('NFC', ስም) != ስም:
        raise SystemExit('መለያ_እሴት_5b7b8b77 또는 አጠናቅር_እሴት ስህተት: ' + str(መተላለፊያ))
    ምንጭ = መተላለፊያ.read_text(encoding='utf-8')
    እወጃ = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ምንጭ)
    if እወጃ and እወጃ.group(1) != ስም:
        raise SystemExit('ፋይል·공개 ቅርጸት_እሴት ስም 불일치: ' + str(መተላለፊያ))
print('UTF-8 공개 ቅርጸት_እሴት·ፋይል ስም አረጋግጥ 완료; 현지어 검토 상태는 국가판 명명 ውሂብ ማጣቀሻ')
PY
