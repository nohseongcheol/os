#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/利用者空間構築.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('利用者空間構築', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('利用者空間構築')
    対応付け値 = {'mode': 'メソッド方式', 'header': 'ヘッダー値', 'i': '序数添字', 'build_ccompiler': 'Cコンパイラ作成', 'ar': '書庫道具要素', 'posix': 'POSIX', 'payload': '本文データデータ', 'flags': '構成設定ビット列', 'cases': '場合試験', 'cc': 'Cコンパイラ', 'data': 'データ', 'build_java_library': 'Javaライブラリ作成', 'ld': '連結器道具要素', 'repo': '保管庫経路', 'build_python': 'Python作成', 'inc': '包含経路', 'argument': '転送済み値', 'text': '文', 'headers': 'ヘッダー一覧', 'cxx': 'Cppコンパイラ', 'valid': '妥当', 'build': '構築', 'build_users': '利用者空間作成', 'compiler': 'コンパイラ道具要素', 'uzlib': '解凍ライブラリ', 'extra': '追加分領域', 'phoff': 'プログラムヘッダー変位量', 'offset': '変位量値', 'text_address': '命令番地', 'abi': '呼出しABI', 'assembly': 'アセンブリ', 'run': '命令実行', 'path': '経路', 'p': 'データ位置', 'changed': '変更済み', 'n': '項目個数', 'flag': '設定値値', 'index': '検索添字', 'classes': 'クラス経路', 'output': '出力結果', 'loads': '読込項目', 'data_address': 'データ番地', 'symbol': '記号値', 'root': '根番地', 'patches': '変更一覧', 'source': '原本データ', 'sizes': '容量一覧', 'blobs': '二進資料群', 'name': '名前', 'value': '値', 'fmt': 'データ書式', 'work': '作業中経路'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
