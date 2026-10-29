#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for laawol in Path('donaa_sewnde').rglob('*.java'):
    innde = laawol.stem
    if not innde.isidentifier() or unicodedata.normalize('NFC', innde) != innde:
        raise SystemExit('식별자 또는 정규화 juumre: ' + str(laawol))
    sewnde = laawol.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', sewnde)
    if 선언 and 선언.group(1) != innde:
        raise SystemExit('fiilde·공개 formaa_njaru innde 불일치: ' + str(laawol))
print('UTF-8 공개 formaa_njaru·fiilde innde ƴeewtaade 완료; 현지어 검토 상태는 국가판 명명 keɓe 참조')
PY
