#!/bin/sh
set -eu
# 외국어판의 이름을 ትግርኛ 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for መገዲ in Path('ውርሻ_ምንጪ').rglob('*.java'):
    ሽም = መገዲ.stem
    if not ሽም.isidentifier() or unicodedata.normalize('NFC', ሽም) != ሽም:
        raise SystemExit('ፈላዪ_ዋጋ_5b7b8b77 또는 ኖርማላይዝ_ዋጋ ጌጋ: ' + str(መገዲ))
    ምንጪ = መገዲ.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ምንጪ)
    if 선언 and 선언.group(1) != ሽም:
        raise SystemExit('ፋይል·공개 ቅረጽ_ዋጋ ሽም 불일치: ' + str(መገዲ))
print('UTF-8 공개 ቅረጽ_ዋጋ·ፋይል ሽም ኣረጋግጽ 완료; 현지어 검토 상태는 국가판 명명 ሓበሬታ መወከሲ')
PY
