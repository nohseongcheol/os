#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/SDKコンパイル.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('SDKコンパイル', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('SDKコンパイル')
    対応付け値 = {'compiler': 'コンパイラ道具要素', 'obj': '宛先ファイル', 'sdk': '開発道具一式', 'output': '出力結果', 'main': '起動処理', 'elf': '実行形式ファイル', 'is_c': '判定C言語', 'parser': '引数解析器', 'language': '言語', 'work': '作業中経路', 'args': '引数配列'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
