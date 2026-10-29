#!/bin/sh
set -eu
# 외국어판의 이름을 français 전용 규칙으로 거부하지 않는다.
# valeurSens·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for chemin in Path('SourcesFondamentales').rglob('*.java'):
    nom = chemin.stem
    if not nom.isidentifier() or unicodedata.normalize('NFC', nom) != nom:
        raise SystemExit('valeurIdentificateur 또는 normaliserValeur erreur: ' + str(chemin))
    source = chemin.read_text(encoding='utf-8')
    Déclarations = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', source)
    if Déclarations and Déclarations.group(1) != nom:
        raise SystemExit('Fichier·공개 valeurFormat nom 불일치: ' + str(chemin))
print('UTF-8 공개 valeurFormat·Fichier nom vérifier estTerminé; 현지어 검토 상태는 국가판 nommage Données référence')
PY
