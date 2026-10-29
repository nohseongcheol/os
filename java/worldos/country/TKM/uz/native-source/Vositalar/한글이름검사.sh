#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for yo_l in Path('meros_manba').rglob('*.java'):
    Nomi = yo_l.stem
    if not Nomi.isidentifier() or unicodedata.normalize('NFC', Nomi) != Nomi:
        raise SystemExit('identifikator_VALUE 또는 normallashtirmoq_VALUE Xato: ' + str(yo_l))
    manba = yo_l.read_text(encoding='utf-8')
    e_lon_qilish = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', manba)
    if e_lon_qilish and e_lon_qilish.group(1) != Nomi:
        raise SystemExit('Fayl·공개 format_VALUE Nomi 불일치: ' + str(yo_l))
print('UTF-8 공개 format_VALUE·Fayl Nomi tasdiqlamoq 완료; 현지어 검토 상태는 국가판 명명 ma_lumotlar Ma_lumotnomalar')
PY
