#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for يونلور in Path('پاتشونى_سرچینه').rglob('*.java'):
    نوم = يونلور.stem
    if not نوم.isidentifier() or unicodedata.normalize('NFC', نوم) != نوم:
        raise SystemExit('식별자 또는 لیوی_کول_ارزښت تېروتنه: ' + str(يونلور))
    سرچينه = يونلور.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', سرچينه)
    if 선언 and 선언.group(1) != نوم:
        raise SystemExit('دوتنه·공개 بڼه_ارزښت نوم 불일치: ' + str(يونلور))
print('UTF-8 공개 بڼه_ارزښت·دوتنه نوم 확인 완료; 현지어 검토 상태는 국가판 명명 اومتوک 참조')
PY
