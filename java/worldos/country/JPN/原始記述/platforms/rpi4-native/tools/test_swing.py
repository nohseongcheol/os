#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/画面部品試験.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('画面部品試験', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('画面部品試験')
    対応付け値 = {'wait': '待機', 'x': '横座標', 's': '文字列データ', 'i': '序数添字', 'sel': '選択器', 'seconds': '秒数単位', 'log': '履歴記録記録', 'data': 'データ', 'at': '現在位置', 'send': '送信', 'main': '起動処理', 'req': '要求値', 'hot': '短縮操作値', 'pump': '取扱いイベント', 'ROOT': '計画根', 'marker': '標識', 'b': '第二値', 'command': '命令', 'shell': 'シェル', 'f': 'ファイル入口', 'click': 'クリックボタン', 'k': '第三添字', 'c': '文字コード', 'r': '返却済み値', 'p': 'データ位置', 'command_mode': '命令方式', 'end': '終端位置変位量', 'classes': 'クラス経路', 'key': '押下済み値', 'y': '縦座標', 'result': '結果', 'report': '妥当性報告', 'dest': '宛先値位置', 'work': '作業中経路', 'qmp': '試験用模擬制御接続状態'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
