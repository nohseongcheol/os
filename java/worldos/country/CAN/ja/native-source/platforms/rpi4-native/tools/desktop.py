#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/デスクトップ表示像.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('デスクトップ表示像', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('デスクトップ表示像')
    対応付け値 = {'count': '入口個数', 'special': '特殊キー', 'error': 'エラー', 'exact': '厳密値', 'network': '通信使用', 'closed': '判定閉鎖済み', 'length': '長さ', 'opened': '開放済み', 'ftp_port': 'ファイル転送ポート番号', 'server': 'サーバー値', 'resources': '資源一覧', 'data': 'データ', 'shift': 'シフトキー', 'send': '送信', 'run_desktop': 'デスクトップ起動処理', 'protocol': '通信網ABI', 'forwards': '転送中規則一覧', 'host': 'ホスト', 'text': '文', 'korean': '韓国語', 'port': 'ポート番号', 'signum': '信号番号', 'version': '版番号', 'parser': '引数解析器', 'bridge': '橋渡し', 'kind': '分類値', 'tail': '終端部分', 'size': '容量', 'previous_buttons': '前回ボタン一覧', 'key': '押下済み値', 'y': '縦座標', 'prefix': '先行部分', 'client': '接続元', 'char': '文字データ', 'work': '作業中経路', 'Keyboard': 'キーボード', 'x': '横座標', 'down': '判定押下中', 'net': '通信網橋渡し入口', 'self': '自身値', 'mode_changed': '方式変更済み', 'serial': '直列入出力', 'args': '引数配列', 'Hangul': 'ハングル合成', 'chunk': '断片値', 'proc': 'プロセス', 'Desktop': 'デスクトップ接続', 'buttons': 'ボタン一覧', 'thread': '作業担当', 'pressed': '判定押下済み', 'previous': '前回', 'toggle': '切替方式', 'command': '命令', 'sock': 'ソケット値', 'frame': '実行状態枠組', 'ctrl': '制御キー', 'path': '経路', 'cp': '文字符号化状態', 'terminate': '終了', 'security': '安全性', 'vnc_port': 'VNCポート', 'body': '本体本文', 'index': '検索添字', 'exited': '保有終了済み', 'keysym': 'キー記号', 'output': '出力結果', 'keyboard': 'キーボード入口', 'interrupted': '中断済み', 'listener': 'ポート受取', 'reader': '読取器', 'NetworkBridge': '通信網橋渡し', 'gui': '描画中画面', 'worker': '処理工程作業'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
