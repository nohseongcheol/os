#!/bin/sh
set -eu
# 외국어판의 이름을 español 전용 규칙으로 거부하지 않는다.
# valorSignificado·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for ruta in Path('FuentesFundamentales').rglob('*.java'):
    nombre = ruta.stem
    if not nombre.isidentifier() or unicodedata.normalize('NFC', nombre) != nombre:
        raise SystemExit('valorIdentificador 또는 normalizarValor error: ' + str(ruta))
    fuente = ruta.read_text(encoding='utf-8')
    Declaraciones = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', fuente)
    if Declaraciones and Declaraciones.group(1) != nombre:
        raise SystemExit('Archivo·공개 valorFormato nombre 불일치: ' + str(ruta))
print('UTF-8 공개 valorFormato·Archivo nombre verificar esTerminado; 현지어 검토 상태는 국가판 denominación Datos referencia')
PY
