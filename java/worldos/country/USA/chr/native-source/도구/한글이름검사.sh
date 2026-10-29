#!/bin/sh
set -eu
# 외국어판의 이름을 한국어 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for ᎠᏍᏓᏩᏛᏍᏗ in Path('ᏄᏛᏁᎵᏙᎸ_ᎠᏰᎸᎯ_ᎦᏟᏌᏅᎯ').rglob('*.java'):
    ᏚᏙᎥᎢ = ᎠᏍᏓᏩᏛᏍᏗ.stem
    if not ᏚᏙᎥᎢ.isidentifier() or unicodedata.normalize('NFC', ᏚᏙᎥᎢ) != ᏚᏙᎥᎢ:
        raise SystemExit('ᎠᏓᏙᎵᎩ_ᏧᎬᏩᎶᏗᏯ 또는 정규화 ᎦᎵᏓᏍᏔᏅ: ' + str(ᎠᏍᏓᏩᏛᏍᏗ))
    ᎦᏟᏌᏅᎯ_0201f362 = ᎠᏍᏓᏩᏛᏍᏗ.read_text(encoding='utf-8')
    선언 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ᎦᏟᏌᏅᎯ_0201f362)
    if 선언 and 선언.group(1) != ᏚᏙᎥᎢ:
        raise SystemExit('ᎠᏍᏆᏂᎪᏙᏗ·공개 ᏱᎬᏁᎸᎯ_ᏧᎬᏩᎶᏗᏯ ᏚᏙᎥᎢ 불일치: ' + str(ᎠᏍᏓᏩᏛᏍᏗ))
print('UTF-8 공개 ᏱᎬᏁᎸᎯ_ᏧᎬᏩᎶᏗᏯ·ᎠᏍᏆᏂᎪᏙᏗ ᏚᏙᎥᎢ ᎰᎯᏳᏓ 완료; 현지어 검토 상태는 국가판 명명 ᎦᏟᏌᏅᎯ 참조')
PY
