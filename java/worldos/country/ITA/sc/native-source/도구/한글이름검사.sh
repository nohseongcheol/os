#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for 경로 in Path('원천').rglob('*.java'):
    Nùmene = 경로.stem
    if not Nùmene.isidentifier() or unicodedata.normalize('NFC', Nùmene) != Nùmene:
        raise SystemExit('식별자 또는 정규화 오류: ' + str(경로))
    원문 = 경로.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', 원문)
    if 선언 and 선언.group(1) != Nùmene:
        raise SystemExit('파일·공개 형식 Nùmene 불일치: ' + str(경로))
print('UTF-8 공개 형식·파일 Nùmene 확인 완료; 현지어 검토 상태는 국가판 명명 자료 참조')
PY
