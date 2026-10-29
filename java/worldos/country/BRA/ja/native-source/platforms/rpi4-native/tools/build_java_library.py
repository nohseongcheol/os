#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/Javaライブラリ構築.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('Javaライブラリ構築', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('Javaライブラリ構築')
    対応付け値 = {'header': 'ヘッダー値', 'sources': 'ソース一覧', 'i': '序数添字', 'info': 'システム情報', 'payload': '本文データデータ', 'src': '原本番地', 'run': '命令実行', 'build_java_library': 'Javaライブラリ作成', 'relative': '相対経路', 'classes': 'クラス経路', 'dist': '配布経路', 'archive': '書庫', 'output': '出力結果', 'root': '根番地', 'name': '名前', 'jar': 'Java束', 'b': '第二値', 'entries': '登録項目一覧一覧'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
