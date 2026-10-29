#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for Ýol in Path('geçen_gor').rglob('*.java'):
    Ad = Ýol.stem
    if not Ad.isidentifier() or unicodedata.normalize('NFC', Ad) != Ad:
        raise SystemExit('tanaýjy_baha 또는 adaty_ýagdaýa_getir_baha Hata: ' + str(Ýol))
    Çeşme = Ýol.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', Çeşme)
    if 선언 and 선언.group(1) != Ad:
        raise SystemExit('Faýl·공개 format_baha Ad 불일치: ' + str(Ýol))
print('UTF-8 공개 format_baha·Faýl Ad barla 완료; 현지어 검토 상태는 국가판 명명 maglumat Salgylanma')
PY
