#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for njia in Path('kirithi_chanzo').rglob('*.java'):
    Jina = njia.stem
    if not Jina.isidentifier() or unicodedata.normalize('NFC', Jina) != Jina:
        raise SystemExit('kitambulishi_thamani 또는 kawaidisha_thamani kosa: ' + str(njia))
    chanzo = njia.read_text(encoding='utf-8')
    tamko = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', chanzo)
    if tamko and tamko.group(1) != Jina:
        raise SystemExit('faili·공개 umbiza_thamani Jina 불일치: ' + str(njia))
print('UTF-8 공개 umbiza_thamani·faili Jina thibitisha 완료; 현지어 검토 상태는 국가판 명명 data Marejeleo')
PY
