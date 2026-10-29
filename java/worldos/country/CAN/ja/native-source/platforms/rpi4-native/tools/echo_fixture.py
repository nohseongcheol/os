#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/復唱試験資料.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('復唱試験資料', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('復唱試験資料')
    対応付け値 = {'data': 'データ', 'e': '補助入口', 'connection': '接続状態', 'f': 'ファイル入口', 'peer': '通信相手値', 'self': '自身値', 'udp': 'データグラム制御', 't': '端末入口', 'tcp': '接続状態制御', 'EchoFixture': '復唱試験資料', 'args': '引数配列', 'chunk': '断片値'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
