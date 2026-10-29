#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/用例集構築.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('用例集構築', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('用例集構築')
    対応付け値 = {'out': '結果データ', 'build_examples': '用例集作成', 'files': 'ファイル一覧', 'java': 'Java実行', 'run': '命令実行', 'path': '経路', 'p': 'データ位置', 'readme': '案内書', 'build_java_library': 'Javaライブラリ作成', 'code': '命令語列順', 'index': '検索添字', 'classes': 'クラス経路', 'repo': '保管庫経路', 'root': '根番地', 'content': '内容物値', 'source': '原本データ', 'name': '名前', 'target': '対象値', 'manifest': '束管理目録', 'language': '言語'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
