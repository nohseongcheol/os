#!/bin/sh
set -eu
# 외국어판의 이름을 Galego 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for CAMIÑO in Path('herdado_fonte').rglob('*.java'):
    Nome = CAMIÑO.stem
    if not Nome.isidentifier() or unicodedata.normalize('NFC', Nome) != Nome:
        raise SystemExit('식별자 또는 organizar_VALOR ERRO: ' + str(CAMIÑO))
    FONTE = CAMIÑO.read_text(encoding='utf-8')
    declaración = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', FONTE)
    if declaración and declaración.group(1) != Nome:
        raise SystemExit('Ficheiro·공개 formato_VALOR Nome 불일치: ' + str(CAMIÑO))
print('UTF-8 공개 formato_VALOR·Ficheiro Nome verificar 완료; 현지어 검토 상태는 국가판 명명 datos Material_de_referencia')
PY
