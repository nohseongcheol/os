#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for ЗАМ in Path('хуучин_эх').rglob('*.java'):
    Нэр = ЗАМ.stem
    if not Нэр.isidentifier() or unicodedata.normalize('NFC', Нэр) != Нэр:
        raise SystemExit('танигч_утга 또는 нормчлох_утга Алдаа: ' + str(ЗАМ))
    ЭХ = ЗАМ.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ЭХ)
    if 선언 and 선언.group(1) != Нэр:
        raise SystemExit('Файл·공개 формат_утга Нэр 불일치: ' + str(ЗАМ))
print('UTF-8 공개 формат_утга·Файл Нэр шалгах 완료; 현지어 검토 상태는 국가판 명명 өгөгдөл Толь_лавлах')
PY
