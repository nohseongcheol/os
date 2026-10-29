#!/usr/bin/env python3
"""기존 経路 호환 入口点. 実際データ 実装: ../道具/イメージ作成.py"""
import importlib as 取得処理値
import sys as 稼働システム値
from pathlib import Path as 経路
稼働システム値.path.insert(0, str(経路(__file__).resolve().parents[1] / '道具'))
if __name__ == '__main__':
    import runpy as プログラム実行器
    プログラム実行器.run_module('イメージ作成', run_name='__main__', alter_sys=True)
else:
    実装 = 取得処理値.import_module('イメージ作成')
    対応付け値 = {'total': '合計容積', 'start': '起動処理', 'firmware': '機器制御コード値', 'files': 'ファイル一覧', 'archive_base': '書庫基底', 'partition': '分割ファイル', 'archive': '書庫', 'main': '起動処理', 'block': 'データブロック', 'ROOT': '計画根', 'boot': '起動経路', 'stage': '工程値', 'out': '結果データ', 'expected': '期待', 'f': 'ファイル入口', 'src': '原本番地', 'path': '経路', 'p': 'データ位置', 'extracted': '抽出済み', 'member': '成員', 'mbr': '主担当起動記録', 'image': 'イメージ', 'sector_count': '扇区個数', 'dist': '配布経路', 'sha': 'ハッシュ計算', 'license_': '利用許諾', 'source': '原本データ', 'name': '名前', 'value': '値', 'manifest': '束管理目録', 'dest': '宛先値位置', 'work': '作業中経路'}
    for 前回項目, 現在項目 in 対応付け値.items():
        if hasattr(実装, 現在項目): globals()[前回項目] = getattr(実装, 現在項目)
