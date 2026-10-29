#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/上傳檔案集.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('上傳檔案集', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('上傳檔案集')
    映射值 = {'data': '資料', 'i': '序數索引', 'name': '名稱', 'c': '字元程式碼', 'p': '資料位置', 'args': '實際參數陣列'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
