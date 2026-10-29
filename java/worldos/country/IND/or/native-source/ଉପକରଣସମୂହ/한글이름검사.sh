#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for ପଥ in Path('ଲିଗାସୀ_ଉତ୍ସ').rglob('*.java'):
    ନାମ = ପଥ.stem
    if not ନାମ.isidentifier() or unicodedata.normalize('NFC', ନାମ) != ନାମ:
        raise SystemExit('ପରିଚାୟକ_ମୂଲ୍ୟ 또는 ସ୍ୱାଭାବିକ_ମୂଲ୍ୟ ତ୍ରୁଟି: ' + str(ପଥ))
    ଉତ୍ସ = ପଥ.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ଉତ୍ସ)
    if 선언 and 선언.group(1) != ନାମ:
        raise SystemExit('ଫାଇଲ·공개 ଫର୍ମାଟ୍_ମୂଲ୍ୟ ନାମ 불일치: ' + str(ପଥ))
print('UTF-8 공개 ଫର୍ମାଟ୍_ମୂଲ୍ୟ·ଫାଇଲ ନାମ ଯାଞ୍ଚ୍_କରିବା 완료; 현지어 검토 상태는 국가판 명명 ଡାଟା ପ୍ରସଙ୍ଗ')
PY
