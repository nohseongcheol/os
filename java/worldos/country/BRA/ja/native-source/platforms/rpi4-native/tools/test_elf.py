#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/ELF試験.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('ELF試験', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('ELF試験')
    対応付け値 = {'out': '結果データ', 'expected': '期待', 'phoff': 'プログラムヘッダー変位量', 'offset': '変位量値', 'invalid': '無効データ', 'path': '経路', 'executable': '実行形式イメージ', 'rejected': '却下状態結果', 'linux_example': 'Linux例', 'original': '原本', 'result': '結果', 'format_': '書式指定', 'main': '起動処理', 'content': '内容物値', 'source': '原本データ', 'name': '名前', 'reference': '比較状態基準線', 'ROOT': '計画根', 'value': '値', 'report': '妥当性報告'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
