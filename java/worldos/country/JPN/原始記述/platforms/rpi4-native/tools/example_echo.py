#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/復唱試験サーバー.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('復唱試験サーバー', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('復唱試験サーバー')
    対応付け値 = {'data': 'データ', 'sock': 'ソケット値', 'tcp_port': 'TCPポート', 'chunk': '断片値', 'received': '保有受信済み', 'self': '自身値', 'UDP': 'データグラム取扱い要求', 'thread': '作業担当', 'echo': '復唱サーバー入口', 'TCP': '取扱い接続状態要求', 'EchoServers': '復唱サーバー一覧', 'parser': '引数解析器', 'server': 'サーバー値', 'udp_port': 'UDPポート', 'args': '引数配列'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
