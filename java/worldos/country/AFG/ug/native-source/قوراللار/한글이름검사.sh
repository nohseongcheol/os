#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for يول in Path('كونا_مەنبە').rglob('*.java'):
    ئاتى = يول.stem
    if not ئاتى.isidentifier() or unicodedata.normalize('NFC', ئاتى) != ئاتى:
        raise SystemExit('پەرقلەندۈرگۈچ_قىممىتى 또는 نورماللاشتۇرماق_قىممىتى خاتالىق: ' + str(يول))
    مەنبە = يول.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', مەنبە)
    if 선언 and 선언.group(1) != ئاتى:
        raise SystemExit('ھۆججەت·공개 فورمات_قىممىتى ئاتى 불일치: ' + str(يول))
print('UTF-8 공개 فورمات_قىممىتى·ھۆججەت ئاتى دەلىللىمەك 완료; 현지어 검토 상태는 국가판 명명 مەلۇمات پايدىلانما')
PY
