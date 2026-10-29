#!/bin/sh
set -eu
# 외국어판의 이름을 ಕನ್ನಡ 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for ಮಾರ್ಗ in Path('ಲೆಗಸಿ_ಮೂಲ').rglob('*.java'):
    ಹೆಸರು = ಮಾರ್ಗ.stem
    if not ಹೆಸರು.isidentifier() or unicodedata.normalize('NFC', ಹೆಸರು) != ಹೆಸರು:
        raise SystemExit('ಗುರುತಿಸುವಿಕೆ_ಮೌಲ್ಯ 또는 ಸಮಾನೀಕರಿಸು_ಮೌಲ್ಯ ದೋಷ: ' + str(ಮಾರ್ಗ))
    ಮೂಲ = ಮಾರ್ಗ.read_text(encoding='utf-8')
    ದೃಢೀಕರಣ = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ಮೂಲ)
    if ದೃಢೀಕರಣ and ದೃಢೀಕರಣ.group(1) != ಹೆಸರು:
        raise SystemExit('ಕಡತ·공개 ಸ್ವರೂಪ_ಮೌಲ್ಯ ಹೆಸರು 불일치: ' + str(ಮಾರ್ಗ))
print('UTF-8 공개 ಸ್ವರೂಪ_ಮೌಲ್ಯ·ಕಡತ ಹೆಸರು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು 완료; 현지어 검토 상태는 국가판 명명 ಡೇಟಾ ಉಲ್ಲೇಖ')
PY
