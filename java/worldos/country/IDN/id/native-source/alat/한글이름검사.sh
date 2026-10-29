#!/bin/sh
set -eu
# 외국어판의 이름을 Indonesia 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for jalur in Path('lama_sumber').rglob('*.java'):
    Nama_2 = jalur.stem
    if not Nama_2.isidentifier() or unicodedata.normalize('NFC', Nama_2) != Nama_2:
        raise SystemExit('pengidentifikasi_VALUE 또는 normalkan_VALUE galat: ' + str(jalur))
    kodeSumber = jalur.read_text(encoding='utf-8')
    deklarasi_4f4f026b = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', kodeSumber)
    if deklarasi_4f4f026b and deklarasi_4f4f026b.group(1) != Nama_2:
        raise SystemExit('berkas·공개 format_VALUE Nama_2 불일치: ' + str(jalur))
print('UTF-8 공개 format_VALUE·berkas Nama_2 periksa 완료; 현지어 검토 상태는 국가판 명명 data Referensi')
PY
