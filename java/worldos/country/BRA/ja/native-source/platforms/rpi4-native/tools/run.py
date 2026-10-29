#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/命令実行.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('命令実行', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('命令実行')
    対応付け値 = {'supported': '対応済み機能一覧', 'parser': '引数解析器', 'qemu': '試験用模擬機械', 'run_desktop': 'デスクトップ起動処理', 'main': '起動処理', 'host': 'ホスト', 'status': '状況値', 'NetworkBridge': '通信網橋渡し', 'ROOT': '計画根', 'bridge': '橋渡し', 'loader': 'ローダー', 'base': '背景値', 'options': '選択項目', 'binary': '二進', 'args': '引数配列', 'command': '命令'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
