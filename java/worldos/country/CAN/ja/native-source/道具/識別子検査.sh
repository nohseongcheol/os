#!/bin/sh
set -eu
# 외국어판의 이름을 日本語 전용 규칙으로 거부하지 않는다.
# 意味値·어원 검토 여부는 native-pending.tsv와 native-term-evidence.json에 기록한다.
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata
for 経路 in Path('基幹ソース').rglob('*.java'):
    名前 = 経路.stem
    if not 名前.isidentifier() or unicodedata.normalize('NFC', 名前) != 名前:
        raise SystemExit('識別子値 또는 値正規化 エラー: ' + str(経路))
    ソース = 経路.read_text(encoding='utf-8')
    宣言 = re.search(r'public\s+(?:(?:final|abstract)\s+)?(?:class|interface|enum)\s+([^\s<{]+)', ソース)
    if 宣言 and 宣言.group(1) != 名前:
        raise SystemExit('ファイル·공개 書式値 名前 불일치: ' + str(経路))
print('UTF-8 공개 書式値·ファイル 名前 検証 判定完了; 현지어 검토 상태는 국가판 命名 データ 参照')
PY
