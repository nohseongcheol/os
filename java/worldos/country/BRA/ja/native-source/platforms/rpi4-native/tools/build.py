#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/システム構築.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('システム構築', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('システム構築')
    対応付け値 = {'network': '通信使用', 'BUILD': '経路構築', 'ar': '書庫道具要素', 'build_examples': '用例集作成', 'posix': 'POSIX', 'font_data': '書体データ', 'flags': '構成設定ビット列', 'a': '先頭位置値', 'cc': 'Cコンパイラ', 'args': '引数配列', 'source_flags': '原本構成設定', 'ld': '連結器道具要素', 'method': 'メソッド入口', 'main': '起動処理', 'objcopy': 'オブジェクトファイル変換器', 'ROOT': '計画根', 'cxx': 'Cppコンパイラ', 'includes': '包含引数', 'compiler': 'コンパイラ道具要素', 'build_users': '利用者空間作成', 'f': 'ファイル入口', 'extra': '追加分領域', 'exports': '公開表', 'jobs': '仕事一覧構築', 'run': '命令実行', 'path': '経路', 'REPO': '保管庫根', 'tool': '道具', 'classes': 'クラス経路', 'output': '出力結果', 'samples': '例登録項目一覧', 'symbol': '記号値', 'source': '原本データ', 'name': '名前', 'build_network': '通信網作成', 'font_info': '書体情報', 'manifest': '束管理目録', 'work': '作業中経路'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
