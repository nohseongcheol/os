#!/usr/bin/env python3
"""内蔵 Java 局所有効範囲 이름을 바꾼다. 文字列·주석·外部値 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

計画根 = Path(__file__).resolve().parents[1]
対応付け値 = json.loads((計画根 / '命名/Java名前一覧.json').read_text())
断片要素式 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
履歴記録記録 = []
for ディレクトリ値 in ('ソース', '利用者/Java', '日本語Java'):
    for 経路 in sorted((計画根 / ディレクトリ値).rglob('*.java')):
        ソース = 経路.read_text()
        断片一覧一覧 = list(断片要素式.finditer(ソース))
        使用済み名前 = {断片要素入口.group() for 断片要素入口 in 断片一覧一覧 if re.search('[先頭位置被演算子-힣]', 断片要素入口.group())}
        ファイル対応付け = {}
        for 前回項目, 後続側値 in 対応付け値.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            新規名前 = 後続側値
            while 新規名前 in 使用済み名前: 新規名前 = '局所有効範囲' + 新規名前
            ファイル対応付け[前回項目] = 新規名前
        値改変 = []
        前回断片要素 = ''
        for 断片要素入口 in 断片一覧一覧:
            字句用語 = 断片要素入口.group()
            if 字句用語.startswith(('//', '/*', '"', "'")): continue
            if 字句用語 in ファイル対応付け and 前回断片要素 != '.':
                値改変.append((断片要素入口.start(), 断片要素入口.end(), ファイル対応付け[字句用語]))
                履歴記録記録.append((str(経路.relative_to(計画根)), 字句用語, ファイル対応付け[字句用語]))
            前回断片要素 = 字句用語
        for 起動処理, 終端, 新規名前 in reversed(値改変): ソース = ソース[:起動処理] + 新規名前 + ソース[終端:]
        if 値改変: 経路.write_text(ソース)
(計画根 / '命名/Java名前対応付け.tsv').write_text('ファイル\t이전\t이후\n' + ''.join('\t'.join(入口値)+'\n' for 入口値 in sorted(set(履歴記録記録))))
print('Java 名前 参照 値変更:', len(履歴記録記録))
