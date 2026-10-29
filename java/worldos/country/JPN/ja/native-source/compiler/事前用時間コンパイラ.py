#!/usr/bin/env python3
"""前回項目 Python 경로를 Java 미리 번역기에 연결한다. ソース翻訳処理 구현은 Java道具/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from コンパイラ import 翻訳工程エラー

計画根 = Path(__file__).resolve().parent

class 機械コードコンパイラ:
    def __init__(自身値, 入力クラス群, 実行状態対象='kernel', ヒープ語個数=262144):
        自身値.経路一覧 = [データ.経路 for データ in 入力クラス群]
        自身値.実行状態対象 = 実行状態対象
        自身値.ヒープ語個数 = ヒープ語個数

    def 生成(自身値, 入口点, 公開登録項目一覧, 汎用文字表記=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 作業:
            結果経路 = Path(作業)/'generated.c'
            命令 = ['sh', str(計画根/'事前用時間.sh'), '--entry', 入口点,
                    '--profile', 自身値.実行状態対象, '--heap-words', str(自身値.ヒープ語個数), '-o', str(結果経路)]
            if 汎用文字表記: 命令.append('--ucn')
            for 代入値 in 公開登録項目一覧: 命令.extend(['--export', 代入値])
            命令.extend(str(経路) for 経路 in 自身値.経路一覧)
            結果 = subprocess.run(命令, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if 結果.returncode: raise 翻訳工程エラー(結果.stderr.decode('utf-8', 'replace'))
            return 結果経路.read_text()

def 起動処理():
    raise SystemExit(subprocess.call(['sh', str(計画根/'事前用時間.sh')] + sys.argv[1:]))

if __name__ == '__main__': 起動処理()
