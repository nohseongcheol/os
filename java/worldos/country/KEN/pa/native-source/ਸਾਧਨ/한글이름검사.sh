#!/bin/sh
set -eu
# 외국어판의 이름을 ਪੰਜਾਬੀ 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for ਮਾਰਗ in Path('ਲੀਗੇਸੀ_ਸਰੋਤ').rglob('*.java'):
    ਨਾਂ = ਮਾਰਗ.stem
    if not ਨਾਂ.isidentifier() or unicodedata.normalize('NFC', ਨਾਂ) != ਨਾਂ:
        raise SystemExit('ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ_ਕੀਮਤ 또는 ਸਧਾਰਨ_ਬਨਾਉਣਾ_ਕੀਮਤ ਗਲਤੀ: ' + str(ਮਾਰਗ))
    ਸਰੋਤ = ਮਾਰਗ.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ਸਰੋਤ)
    if 선언 and 선언.group(1) != ਨਾਂ:
        raise SystemExit('ਫਾਇਲ·공개 ਸਰੂਪ_ਕੀਮਤ ਨਾਂ 불일치: ' + str(ਮਾਰਗ))
print('UTF-8 공개 ਸਰੂਪ_ਕੀਮਤ·ਫਾਇਲ ਨਾਂ ਤਸਦੀਕ 완료; 현지어 검토 상태는 국가판 명명 ਸਮੱਗਰੀ ਸੰਦਰਭ')
PY
