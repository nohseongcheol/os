#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/用例集試験.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('用例集試験', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('用例集試験')
    対応付け値 = {'count': '入口個数', 'exact': '厳密値', 'expected_file': '期待ファイル', 'ftp_port': 'ファイル転送ポート番号', 'data': 'データ', 'graphics_command': '描画命令', 'main': '起動処理', 'row': '行番号位置', 'init': '初期値', 'target': '対象値', 'ROOT': '計画根', 'text': '文', 'binary': '二進', 'out': '結果データ', 'entry': '入口点', 'got': '受信済み個数', 'port': 'ポート番号', 'graphics_start': '描画中開始処理', 'col': '列位置', 'begin': '変位量開始処理', 'kind': '分類値', 'selector': '準備監視器', 'n': '項目個数', 'key': '押下済み値', 'y': '縦座標', 'client': '接続元', 'line': '行', 'report': '妥当性報告', 'language': '言語', 'x': '横座標', 'start': '起動処理', 'rgb': 'RGB色', 'down': '判定押下中', 'listing': '一覧送信', 'payload': '本文データデータ', 'proc': 'プロセス', 'w': '要求済み幅値', 'temporary': '一時', 'echo': '復唱サーバー入口', 'label': '名前表', 'content': '内容物値', 'argument': '転送済み値', 'EchoServers': '復唱サーバー一覧', 'marker': '標識', 'expected': '期待', 'test_language': '言語試験', 'filename': 'ファイル入口名前', 'shell': 'シェル', 'color': '画素色', 'transcript': '実行記録', 'offset': '変位量値', 'h': '要求済み高さ値', 'run': '命令実行', 'c': '文字コード', 'path': '経路', 'encoding': '文字設定', 'end': '終端位置変位量', 'ftp': 'ファイル転送接続状態', 'pixels': '画素列一覧', 'symbol': '記号値', 'source': '原本データ', 'name': '名前', 'receive': 'メッセージ受取', 'manifest': '束管理目録'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
