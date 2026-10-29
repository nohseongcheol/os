#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/ファイル実行.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('ファイル実行', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('ファイル実行')
    対応付け値 = {'timeout': '実行状態待機期限', 's': '文字列データ', 'i': '序数添字', 'match': '判定等価', 'files': 'ファイル一覧', 'program': '実行項目', 'executable': '実行形式イメージ', 'args': '引数配列', 'chunk': '断片値', 'data': 'データ', 'proc': 'プロセス', 'send': '送信', 'main': '起動処理', 'marker': '標識', 'command': '命令', 'include': '包含項目', 'dumped': '書出済み', 'run': '命令実行', 'p': 'データ位置', 'parser': '引数解析器', 'options': '選択項目', 'kind': '分類値', 'selector': '準備監視器', 'upload_data': '送出転送データ', 'end': '終端位置変位量', 'n': '項目個数', 'd': '宛先データ', 'key': '押下済み値', 'output': '出力結果', 'line': '行', 'name': '名前', 'upload_name': '送出転送名前', 'receive': 'メッセージ受取'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
