#!/bin/sh
set -eu
# 외국어판의 이름을 中文 전용 규칙으로 거부하지 않는다.
# 含義值·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for 路徑 in Path('基礎原始碼').rglob('*.java'):
    名稱 = 路徑.stem
    if not 名稱.isidentifier() or unicodedata.normalize('NFC', 名稱) != 名稱:
        raise SystemExit('標識符值 또는 正規化值 錯誤: ' + str(路徑))
    原始碼 = 路徑.read_text(encoding='utf-8')
    聲明 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', 原始碼)
    if 聲明 and 聲明.group(1) != 名稱:
        raise SystemExit('檔案·공개 格式值 名稱 불일치: ' + str(路徑))
print('UTF-8 공개 格式值·檔案 名稱 驗證 是否完成; 현지어 검토 상태는 국가판 命名 資料 引用')
PY
