#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/通信網構築.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('通信網構築', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('通信網構築')
    対応付け値 = {'obj': '宛先ファイル', 'objects': '宛先ファイル群', 'library': 'ライブラリ', 'output': '出力結果', 'port': 'ポート番号', 'root': '根番地', 'files': 'ファイル一覧', 'source': '原本データ', 'run': '命令実行', 'flags': '構成設定ビット列', 'path': '経路', 'build_network': '通信網作成', 'cc': 'Cコンパイラ', 'ar': '書庫道具要素'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
