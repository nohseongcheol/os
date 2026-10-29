#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/Cコンパイラ構築.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('Cコンパイラ構築', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('Cコンパイラ構築')
    対応付け値 = {'out': '結果データ', 'builtins': '組込要素群', 'header': 'ヘッダー値', 'sdk': '開発道具一式', 'build_ccompiler': 'Cコンパイラ作成', 'i': '序数添字', 'elf': '実行形式ファイル', 'run': '命令実行', 'flags': '構成設定ビット列', 'path': '経路', 'p': 'データ位置', 'cc': 'Cコンパイラ', 'obj': '宛先ファイル', 'flag': '設定値値', 'ld': '連結器道具要素', 'objects': '宛先ファイル群', 'repo': '保管庫経路', 'v': '一時データ', 'upstream': '上流', 'root': '根番地', 'assets': '素材一覧', 'source': '原本データ', 'name': '名前', 'includes': '包含引数'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
