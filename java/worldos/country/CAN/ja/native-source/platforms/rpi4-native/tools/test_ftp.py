#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/FTP試験.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('FTP試験', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('FTP試験')
    対応付け値 = {'timeout': '実行状態待機期限', 'payload': '本文データデータ', 'broken': '破損', 'linux_example': 'Linux例', 'chunk': '断片値', 'data': 'データ', 'proc': 'プロセス', 'code': '命令語列順', 'linux': 'Linuxファイル', 'archive': '書庫', 'main': '起動処理', 'net_source': '網ソース', 'temporary': '一時', 'static_source': '静的ソース', 'java_source': 'Javaソース', 'echo': '復唱サーバー入口', 'ROOT': '計画根', 'text': '文', 'marker': '標識', 'EchoFixture': '復唱試験資料', 'command': '命令', 'out': '結果データ', 'expected': '期待', 'server_source': 'サーバーソース', 'shell': 'シェル', 'upload': '送出転送ファイル群', 'transcript': '実行記録', 'port': 'ポート番号', 'native': '自前', 'elf': '実行形式ファイル', 'server_udp_port': 'サーバーデータグラムポート', 'packed': '梱包済み', 'bridge': '橋渡し', 'selector': '準備監視器', 'end': '終端位置変位量', 'e': '補助入口', 'ftp': 'ファイル転送接続状態', 'key': '押下済み値', 'bytecode': 'バイトコード', 'peer': '通信相手値', 'result': '結果', 'unchanged': '保持済みデータ', 'line': '行', 'server_tcp_port': 'サーバーストリームポート', 'source': '原本データ', 'NetworkBridge': '通信網橋渡し', 'jar': 'Java束', 'receive': 'メッセージ受取', 'report': '妥当性報告'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
