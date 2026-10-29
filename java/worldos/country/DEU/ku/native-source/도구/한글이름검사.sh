#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for RÊ in Path('원천').rglob('*.java'):
    Nav = RÊ.stem
    if not Nav.isidentifier() or unicodedata.normalize('NFC', Nav) != Nav:
        raise SystemExit('식별자 또는 정규화 Çewtî: ' + str(RÊ))
    ÇAVKANÎ = RÊ.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ÇAVKANÎ)
    if 선언 and 선언.group(1) != Nav:
        raise SystemExit('Pel·공개 형식 Nav 불일치: ' + str(RÊ))
print('UTF-8 공개 형식·Pel Nav 확인 완료; 현지어 검토 상태는 국가판 명명 자료 참조')
PY
