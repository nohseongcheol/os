#!/bin/sh
set -eu
# 외국어판의 이름을 Türkçe 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for yol in Path('eski_kaynak').rglob('*.java'):
    İsim = yol.stem
    if not İsim.isidentifier() or unicodedata.normalize('NFC', İsim) != İsim:
        raise SystemExit('tanımlayıcı_değer 또는 normalleştirmek_değer hata: ' + str(yol))
    kaynakKod = yol.read_text(encoding='utf-8')
    bildirim = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', kaynakKod)
    if bildirim and bildirim.group(1) != İsim:
        raise SystemExit('dosya·공개 biçim_değer İsim 불일치: ' + str(yol))
print('UTF-8 공개 biçim_değer·dosya İsim doğrulamak 완료; 현지어 검토 상태는 국가판 명명 veri Başvuru')
PY
