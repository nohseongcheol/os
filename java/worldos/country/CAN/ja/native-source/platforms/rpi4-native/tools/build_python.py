#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/Python構築.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('Python構築', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('Python構築')
    対応付け値 = {'ld': '連結器道具要素', 'archive': '書庫', 'SHA256': '妥当性ハッシュ', 'build_python': 'Python作成', 'root': '根番地', 'source': '原本データ', 'name': '名前', 'path': '経路', 'VERSION': '言語版値', 'cc': 'Cコンパイラ', 'tar': 'TAR束', 'newlib': 'Newlib包含経路', 'member': '成員'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
