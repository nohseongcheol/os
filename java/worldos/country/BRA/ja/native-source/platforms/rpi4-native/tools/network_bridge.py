#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/通信網橋渡し.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('通信網橋渡し', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('通信網橋渡し')
    対応付け値 = {'response': '応答', 'parts': '経路構成要素', 's': '文字列データ', 'i': '序数添字', 'close': '閉鎖', 'forward': '転送中規則', 'slip_input': 'SLIP入力', 'self': '自身値', 'item': '入口値', 'flags': '構成設定ビット列', 'ftp_port': 'ファイル転送ポート番号', 'args': '引数配列', 'server': 'サーバー値', 'data': 'データ', 'ethernet_input': 'Ethernet入力', 'trace_packet': '追跡パケット', 'GATEWAY': '中継門機器番地', 'rule': '規則値', 'protocol': '通信網ABI', 'forwards': '転送中規則一覧', 'occupied': '占有済み', 'host': 'ホスト', 'ack': '確認状態番号', 'serial_port': '直列ポート番号', 'readers': '読取器群', 'guest': 'ゲスト', 'destination': '宛先データ番地', 'ethernet_port': 'Ethernetポート', 'b': '第二値', 'MAC': '機械番地', 'arp': '番地解像度パケット', 'writable': '書込可能', 'direction': '方向', 'seq': '順序番号', 'frame': '実行状態枠組', 'loop': '周期値', 'port': 'ポート番号', 'offset': '変位量値', 'readable': '可能判定読取', 'c': '文字コード', 'p': 'データ位置', 'writers': '書込器群', 'IP': 'インターネット番地値', 'e': '補助入口', 'n': '項目個数', 'packet': 'パケットデータ', 'arguments': '転送済み引数', 'source': '原本データ', 'NetworkBridge': '通信網橋渡し', 'window': '窓', 'capture': '捕獲'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
