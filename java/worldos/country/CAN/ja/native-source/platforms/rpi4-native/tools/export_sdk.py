#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/公開SDK.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('公開SDK', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('公開SDK')
    対応付け値 = {'out': '結果データ', 'obj': '宛先ファイル', 'relative': '相対経路', 'compiler_archive': 'コンパイラ書庫', 'sdk': '開発道具一式', 'dist': '配布経路', 'archive': '書庫', 'main': '起動処理', 'posix': 'POSIX', 'files': 'ファイル一覧', 'source': '原本データ', 'name': '名前', 'target': '対象値', 'ROOT': '計画根', 'destination': '宛先データ番地', 'manifest': '束管理目録', 'work': '作業中経路'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
