#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/デスクトップ試験.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('デスクトップ試験', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('デスクトップ試験')
    対応付け値 = {'x': '横座標', 'typing': '型付き文字', 'message': '通知本文', 'start': '起動処理', 'down': '判定押下中', 'exact': '厳密値', 'i': '序数添字', 'press': '押下キー', 'rectangles': '矩形一覧一覧', 'sym': '記号', 'j': '内側序数', 'deadline': '期限時間', 'proc': 'プロセス', 'data': 'データ', 'main': '起動処理', 'w': '要求済み幅値', 'init': '初期値', 'block': 'データブロック', 'ROOT': '計画根', 'text': '文', 'marker': '標識', 'report': '妥当性報告', 'until': '到達待ち', 'clipboard': '貼付け板値', 'dst': '宛先番地', 'seen': '確認済み登録項目一覧', 'poll': '準備状態監視器', 'transcript': '実行記録', 'port': 'ポート番号', 'offset': '変位量値', 'h': '要求済み高さ値', 'src': '原本番地', 'event': 'イベント', 'encoding': '文字設定', 'size': '容量', 'key': '押下済み値', 'pixels': '画素列一覧', 'y': '縦座標', 'output': '出力結果', 'symbol': '記号値', 'client': '接続元', 'char': '文字データ', 'rgb': 'RGB色'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
