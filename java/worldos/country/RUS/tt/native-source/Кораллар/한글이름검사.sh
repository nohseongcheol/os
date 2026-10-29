#!/bin/sh
set -eu
# 외국어판의 이름을 Татарча 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for Yul in Path('элекке_чыганак').rglob('*.java'):
    исем = Yul.stem
    if not исем.isidentifier() or unicodedata.normalize('NFC', исем) != исем:
        raise SystemExit('күрсәткеч_VALUE 또는 нормальләштерү_VALUE Хата: ' + str(Yul))
    чыганак = Yul.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', чыганак)
    if 선언 and 선언.group(1) != исем:
        raise SystemExit('Birem·공개 формат_VALUE исем 불일치: ' + str(Yul))
print('UTF-8 공개 формат_VALUE·Birem исем раслау 완료; 현지어 검토 상태는 국가판 명명 мәгълүмат Белешмәлекләр')
PY
