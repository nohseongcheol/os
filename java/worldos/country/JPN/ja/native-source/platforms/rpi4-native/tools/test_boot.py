#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/起動試験.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('起動試験', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('起動試験')
    対応付け値 = {'timeout': '実行状態待機期限', 'response': '応答', 'msg': '通信網メッセージ', 'exact': '厳密値', 'markers': '標識一覧', 'i': '序数添字', 'match': '判定等価', 'execute': '作業実行', 'cancel': '取消処理操作', 'cmd_byte': '命令バイト', 'reply': '返答', 'points': '点一覧', 'server': 'サーバー値', 'data': 'データ', 'prompt': '入力案内', 'enter': '入場', 'imported': '取込済み', 'send': '送信', 'main': '起動処理', 'ROOT': '計画根', 'text': '文', 'first_gui': '先頭位置GUI', 'pixel': '画素', 'java_class': 'Javaクラス', 'upload': '送出転送ファイル群', 'pixels_file': '画素ファイル', 'pixels_data': '画素データ', 'edit': '編集値', 'receive_until': '到達待ち受取', 'selector': '準備監視器', 'size': '容量', 'qmp_path': 'QMP経路', 'key': '押下済み値', 'second_gui': '第二GUI', 'y': '縦座標', 'result': '結果', 'samples': '例登録項目一覧', 'client': '接続元', 'line': '行', 'report': '妥当性報告', 'work': '作業中経路', 'x': '横座標', 'python_checks': 'Python検査項目', 'download': '取得転送', 'greeting': '挨拶例', 'dims': '寸法値', 'chunk': '断片値', 'deadline': '期限時間', 'proc': 'プロセス', 'content': '内容物値', 'block': 'データブロック', 'marker': '標識', 'command': '命令', 'expected': '期待', 'shell': 'シェル', 'drawing': '描画中経路', 'f': 'ファイル入口', 'transcript': '実行記録', 'offset': '変位量値', 'path': '経路', 'screenshot': '画面記録', 'arguments': '転送済み引数', 'pixels': '画素列一覧', 'viewer': '画面接続元', 'output': '出力結果', 'stream': 'ストリーム値', 'cmd': '命令引数列', 'name': '名前', 'qmp': '試験用模擬制御接続状態'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
