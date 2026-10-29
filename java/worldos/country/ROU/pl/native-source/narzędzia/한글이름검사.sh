#!/bin/sh
set -eu
# 외국어판의 이름을 polski 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for ścieżka_2 in Path('starsze_źródło').rglob('*.java'):
    Nazwa = ścieżka_2.stem
    if not Nazwa.isidentifier() or unicodedata.normalize('NFC', Nazwa) != Nazwa:
        raise SystemExit('identyfikator_WARTOŚĆ 또는 normalizować_WARTOŚĆ błąd: ' + str(ścieżka_2))
    plik_źródłowy = ścieżka_2.read_text(encoding='utf-8')
    deklaracja = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', plik_źródłowy)
    if deklaracja and deklaracja.group(1) != Nazwa:
        raise SystemExit('nazwa_pliku·공개 format_WARTOŚĆ Nazwa 불일치: ' + str(ścieżka_2))
print('UTF-8 공개 format_WARTOŚĆ·nazwa_pliku Nazwa 확인 완료; 현지어 검토 상태는 국가판 명명 dane odwołanie')
PY
