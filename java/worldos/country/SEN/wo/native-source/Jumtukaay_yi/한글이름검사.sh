#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for Yoonu_jëmale in Path('ndono_Cosaan').rglob('*.java'):
    tur_253d1510 = Yoonu_jëmale.stem
    if not tur_253d1510.isidentifier() or unicodedata.normalize('NFC', tur_253d1510) != tur_253d1510:
        raise SystemExit('raññeekaay_xëyma 또는 yonnal_xëyma njumte: ' + str(Yoonu_jëmale))
    Cosaan = Yoonu_jëmale.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', Cosaan)
    if 선언 and 선언.group(1) != tur_253d1510:
        raise SystemExit('bara_denc·공개 dayo_xëyma tur_253d1510 불일치: ' + str(Yoonu_jëmale))
print('UTF-8 공개 dayo_xëyma·bara_denc tur_253d1510 luñutu 완료; 현지어 검토 상태는 국가판 명명 mbir Royukaay')
PY
