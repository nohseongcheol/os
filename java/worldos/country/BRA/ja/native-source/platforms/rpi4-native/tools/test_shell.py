#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/シェル試験.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('シェル試験', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('シェル試験')
    対応付け値 = {'timeout': '実行状態待機期限', 'x': '横座標', 'msg': '通信網メッセージ', 'i': '序数添字', 'reply': '返答', 'call': '呼出', 'args': '引数配列', 'chunk': '断片値', 'data': 'データ', 'proc': 'プロセス', 'long_text': '長整数本文', 'restored': '復元済みデータ', 'send': '送信', 'file': 'ファイル', 'main': '起動処理', 'found': '結果捜索', 'ROOT': '計画根', 'text': '文', 'marker': '標識', 'command': '命令', 'expected': '期待', 'pixel': '画素', 'shell': 'シェル', 'poll': '準備状態監視器', 'transcript': '実行記録', 'end': '終端位置変位量', 'image': 'イメージ', 'key': '押下済み値', 'y': '縦座標', 'output': '出力結果', 'result': '結果', 'client': '接続元', 'line': '行', 'stream': 'ストリーム値', 'name': '名前', 'value': '値', 'receive': 'メッセージ受取', 'report': '妥当性報告', 'work': '作業中経路', 'qmp': '試験用模擬制御接続状態'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
