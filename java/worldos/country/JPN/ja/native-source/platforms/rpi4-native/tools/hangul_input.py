#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/ハングル入力.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('ハングル入力', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('ハングル入力')
    対応付け値 = {'old': '前回項目', 'backspace': '後退消去', 'committed': '確定済み', 'KEYS': 'キー配置', 'self': '自身値', 'FINALS': '合成語最終字母', 'VOWELS': '合成語中声字母', 'INITIAL': '初期字母表', 'initial': '初期字母', 'commit': '確定合成状態', 'feed': '供給キー', 'vowel': '中声字母', 'Hangul': 'ハングル合成', 'SPLIT': '最終字母分割処理', 'final': '最終字母', 'key': '押下済み値', 'send': '送信', 'left': '左側面', 'FINAL': '最終字母表', 'history': '履歴', 'pair': '一対', 'char': '文字データ', 'VOWEL': '中声字母表', 'right': '右', 'value': '値', 'text': '文'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
