#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for Hanyar_shiga in Path('Tsohon_Bayani_tushe').rglob('*.java'):
    Suna = Hanyar_shiga.stem
    if not Suna.isidentifier() or unicodedata.normalize('NFC', Suna) != Suna:
        raise SystemExit('mai_ganewa_Daraja 또는 Gajarta_kimar_bayanai_Daraja Kuskure: ' + str(Hanyar_shiga))
    tushe = Hanyar_shiga.read_text(encoding='utf-8')
    bayyanarwa = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', tushe)
    if bayyanarwa and bayyanarwa.group(1) != Suna:
        raise SystemExit('Fayil·공개 zubi_Daraja Suna 불일치: ' + str(Hanyar_shiga))
print('UTF-8 공개 zubi_Daraja·Fayil Suna Tabbatar_da 완료; 현지어 검토 상태는 국가판 명명 Tarin_bayani Manazarta')
PY
