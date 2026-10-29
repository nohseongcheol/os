#!/bin/sh
set -eu
# 외국어판의 이름을 Български 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for ПЪТ in Path('наследен_източник').rglob('*.java'):
    Име = ПЪТ.stem
    if not Име.isidentifier() or unicodedata.normalize('NFC', Име) != Име:
        raise SystemExit('Идентификатор_стойност 또는 нормализирам_стойност ГРЕШКА: ' + str(ПЪТ))
    ИЗТОЧНИК = ПЪТ.read_text(encoding='utf-8')
    декларация = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ИЗТОЧНИК)
    if декларация and декларация.group(1) != Име:
        raise SystemExit('Файл·공개 формат_стойност Име 불일치: ' + str(ПЪТ))
print('UTF-8 공개 формат_стойност·Файл Име проверявам 완료; 현지어 검토 상태는 국가판 명명 данни препратка')
PY
