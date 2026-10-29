#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/端末書体構築.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('端末書体構築', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('端末書体構築')
    対応付け値 = {'data': 'データ', 'img': '描画', 'bits': 'ビット列一覧', 'x': '横座標', 'draw': '画面描画処理', 'licences': '利用許諾一覧', 'paths': '経路一覧', 'y': '縦座標', 'main': '起動処理', 'src': '原本番地', 'fonts': '書体一覧', 'ROOT': '計画根', 'p': 'データ位置', 'cp': '文字符号化状態', 'target': '対象値'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
