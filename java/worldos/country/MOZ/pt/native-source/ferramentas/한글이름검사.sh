#!/bin/sh
set -eu
# 외국어판의 이름을 Português 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for caminho in Path('herdado_fonte').rglob('*.java'):
    Nome = caminho.stem
    if not Nome.isidentifier() or unicodedata.normalize('NFC', Nome) != Nome:
        raise SystemExit('identificador_VALOR 또는 normalizar_VALOR erro: ' + str(caminho))
    códigoFonte = caminho.read_text(encoding='utf-8')
    declaração = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', códigoFonte)
    if declaração and declaração.group(1) != Nome:
        raise SystemExit('ficheiro·공개 formato_VALOR Nome 불일치: ' + str(caminho))
print('UTF-8 공개 formato_VALOR·ficheiro Nome verificar 완료; 현지어 검토 상태는 국가판 명명 dados Referência')
PY
