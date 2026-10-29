#!/bin/sh
set -eu
# 외국어판의 이름을 தமிழ் 전용 규칙으로 거부하지 않는다.
# 뜻·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for பாதை_2 in Path('மரபுவழி_மூலம்').rglob('*.java'):
    பெயர் = பாதை_2.stem
    if not பெயர்.isidentifier() or unicodedata.normalize('NFC', பெயர்) != பெயர்:
        raise SystemExit('அடையாளங்காட்டி_மதிப்பு 또는 சீராக்கு_மதிப்பு பிழை: ' + str(பாதை_2))
    மூலக்_கோப்பு = பாதை_2.read_text(encoding='utf-8')
    அறிவிப்பு = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', மூலக்_கோப்பு)
    if அறிவிப்பு and அறிவிப்பு.group(1) != பெயர்:
        raise SystemExit('கோப்பின்_பெயர்·공개 வடிவமை_மதிப்பு பெயர் 불일치: ' + str(பாதை_2))
print('UTF-8 공개 வடிவமை_மதிப்பு·கோப்பின்_பெயர் பெயர் சரிபார் 완료; 현지어 검토 상태는 국가판 명명 தரவு மேற்கோள்')
PY
