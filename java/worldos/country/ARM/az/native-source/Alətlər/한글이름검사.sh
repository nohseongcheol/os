#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for Cığır in Path('irsi_mənbə').rglob('*.java'):
    Ad = Cığır.stem
    if not Ad.isidentifier() or unicodedata.normalize('NFC', Ad) != Ad:
        raise SystemExit('identifikator_VALUE 또는 normallaşdırmaq_VALUE XƏTA: ' + str(Cığır))
    QAYNAQ = Cığır.read_text(encoding='utf-8')
    bəyannamə = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', QAYNAQ)
    if bəyannamə and bəyannamə.group(1) != Ad:
        raise SystemExit('FAYL·공개 format_VALUE Ad 불일치: ' + str(Cığır))
print('UTF-8 공개 format_VALUE·FAYL Ad yoxlamaq 완료; 현지어 검토 상태는 국가판 명명 verilənlər İstinad')
PY
