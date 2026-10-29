#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/回顯測試夾具.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('回顯測試夾具', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('回顯測試夾具')
    映射值 = {'data': '資料', 'e': '輔助條目', 'connection': '接通狀態', 'f': '檔案條目', 'peer': '對端值', 'self': '自身值', 'udp': '數據報控制', 't': '終端條目', 'tcp': '連接狀態控制', 'EchoFixture': '回顯測試夾具', 'args': '實際參數陣列', 'chunk': '片段值'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
