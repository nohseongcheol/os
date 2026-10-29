#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/測試ELF.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('測試ELF', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('測試ELF')
    映射值 = {'out': '結果資料', 'expected': '預期', 'phoff': '程式標頭偏移', 'offset': '偏移值', 'invalid': '無效資料', 'path': '路徑', 'executable': '可執行文件映像', 'rejected': '拒絕狀態結果', 'linux_example': 'Linux範例', 'original': '原始', 'result': '結果', 'format_': '格式指定', 'main': '運行', 'content': '內容值', 'source': '原始資料', 'name': '名稱', 'reference': '比較基線', 'ROOT': '項目根', 'value': '值', 'report': '有效性驗證報告'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
