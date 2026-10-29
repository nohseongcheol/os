#!/bin/sh
set -eu
# 외국어판의 이름을 Íslenska 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for SLÓÐ in Path('eldra_uppruni').rglob('*.java'):
    Heiti = SLÓÐ.stem
    if not Heiti.isidentifier() or unicodedata.normalize('NFC', Heiti) != Heiti:
        raise SystemExit('auðkenni_VALUE 또는 staðla_VALUE Villa: ' + str(SLÓÐ))
    Uppruni = SLÓÐ.read_text(encoding='utf-8')
    skýrsla = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', Uppruni)
    if skýrsla and skýrsla.group(1) != Heiti:
        raise SystemExit('Skrá·공개 snið_VALUE Heiti 불일치: ' + str(SLÓÐ))
print('UTF-8 공개 snið_VALUE·Skrá Heiti sannprófa 완료; 현지어 검토 상태는 국가판 명명 gögn tilvísun')
PY
