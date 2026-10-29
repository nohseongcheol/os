#!/bin/sh
set -eu
# 외국어판의 이름을 Català 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for Camí in Path('llegat_font').rglob('*.java'):
    Nom = Camí.stem
    if not Nom.isidentifier() or unicodedata.normalize('NFC', Nom) != Nom:
        raise SystemExit('identificador_VALOR 또는 normalitzar_VALOR s_ha_produït_un_error: ' + str(Camí))
    FONT = Camí.read_text(encoding='utf-8')
    declaració = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', FONT)
    if declaració and declaració.group(1) != Nom:
        raise SystemExit('Fitxer·공개 format_VALOR Nom 불일치: ' + str(Camí))
print('UTF-8 공개 format_VALOR·Fitxer Nom verificar 완료; 현지어 검토 상태는 국가판 명명 dades Referència')
PY
