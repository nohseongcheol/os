#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/JVM試験.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('JVM試験', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('JVM試験')
    対応付け値 = {'message': '通知本文', 's': '文字列データ', 'actual': '実際結果', 'match': '判定等価', 'payload': '本文データデータ', 'cases': '場合試験', 'fixture': 'データ試験', 'main': '起動処理', 'ROOT': '計画根', 'text': '文', 'valid': '妥当', 'includes': '包含引数', 'include': '包含項目', 'expected': '期待', 'sources': 'ソース一覧', 'tmp': '一時経路', 'done': '完了済み総量', 'classes': 'クラス経路', 'output': '出力結果', 'result': '結果', 'cmd': '命令引数列', 'name': '名前', 'jar': 'Java束', 'report': '妥当性報告', 'tests': '一覧試験'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
