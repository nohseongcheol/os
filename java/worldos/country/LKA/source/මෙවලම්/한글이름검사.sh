#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for මාර්_ගය in Path('පැවත_එන_මූලය').rglob('*.java'):
    නම = මාර්_ගය.stem
    if not නම.isidentifier() or unicodedata.normalize('NFC', නම) != නම:
        raise SystemExit('හඳුන්වනය_අගය 또는 ප්_රමත_කරන්න_අගය දෝෂය: ' + str(මාර්_ගය))
    මූලය = මාර්_ගය.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', මූලය)
    if 선언 and 선언.group(1) != නම:
        raise SystemExit('ගොනු·공개 හැඩතලය_අගය නම 불일치: ' + str(මාර්_ගය))
print('UTF-8 공개 හැඩතලය_අගය·ගොනු නම තහවුරු_කරන්න 완료; 현지어 검토 상태는 국가판 명명 දත්ත පරිශීලනය')
PY
