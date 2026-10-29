#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/送出転送ファイル群.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('送出転送ファイル群', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('送出転送ファイル群')
    対応付け値 = {'data': 'データ', 'i': '序数添字', 'name': '名前', 'c': '文字コード', 'p': 'データ位置', 'args': '引数配列'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
