#!/bin/sh
set -eu
# 외국어판의 이름을 suomi 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for polku_2 in Path('vanha_lähde').rglob('*.java'):
    Nimi = polku_2.stem
    if not Nimi.isidentifier() or unicodedata.normalize('NFC', Nimi) != Nimi:
        raise SystemExit('tunniste_ARVO 또는 normalisoida_ARVO VIRHE: ' + str(polku_2))
    lähdetiedosto = polku_2.read_text(encoding='utf-8')
    esittely = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', lähdetiedosto)
    if esittely and esittely.group(1) != Nimi:
        raise SystemExit('tiedoston_nimi·공개 muoto_ARVO Nimi 불일치: ' + str(polku_2))
print('UTF-8 공개 muoto_ARVO·tiedoston_nimi Nimi tarkistaa 완료; 현지어 검토 상태는 국가판 명명 data viite')
PY
