#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/ハングル入力試験.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('ハングル入力試験', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('ハングル入力試験')
    対応付け値 = {'expected': '期待', 'Keyboard': 'キーボード', 'press': '押下キー', 'self': '自身値', 'test_modes_repeat_and_commit': '方式一覧反復論理積確定試験', 'keys': '押下済みキー一覧', 'test_paste_and_unicode': '貼付け論理積Unicode試験', 'data': 'データ', 'key': '押下済み値', 'send': '送信', 'test_words': '語一覧試験', 'InputTests': 'ハングル入力試験', 'test_backspace': '後退消去試験', 'symbol': '記号値', 'char': '文字データ', 'type': '型分類'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
