#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/Remmina試験.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('Remmina試験', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('Remmina試験')
    対応付け値 = {'wait': '待機', 'typing': '型付き文字', 'start': '起動処理', 'profile': '動作設定', 'focused': '焦点対象', 'serial': '直列入出力', 'keys': '押下済みキー一覧', 'server': 'サーバー値', 'log': '履歴記録記録', 'args': '引数配列', 'deadline': '期限時間', 'data': 'データ', 'candidate': '候補', 'logs': '履歴記録記録一覧', 'kw': '命名済み引数', 'number': '数値値', 'main': '起動処理', 'ready': '用意状態完了', 'found': '結果捜索', 'guest': 'ゲスト', 'ROOT': '計画根', 'marker': '標識', 'text': '文', 'out': '結果データ', 'env': '環境', 'f': 'ファイル入口', 'port': 'ポート番号', 'offset': '変位量値', 'version': '版番号', 'p': 'データ位置', 'selector': '準備監視器', 'xvfb': '仮想表示処理', 'display': '表示処理装置', 'n': '項目個数', 'key': '押下済み値', 'processes': '稼働状態プロセス一覧', 'rootfs': 'ルートファイル体系', 'xdo': '仮想入力道具要素', 'name': '名前', 'window': '窓', 'report': '妥当性報告', 'work': '作業中経路'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
