#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/導出SDK.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('導出SDK', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('導出SDK')
    映射值 = {'out': '結果資料', 'obj': '目的地址檔案', 'relative': '相對路徑', 'compiler_archive': '編譯器存檔', 'sdk': '開發工具套件', 'dist': '分發路徑', 'archive': '存檔', 'main': '運行', 'posix': 'POSIX', 'files': '檔案列表', 'source': '原始資料', 'name': '名稱', 'target': '目標值', 'ROOT': '項目根', 'destination': '目的地址資料地址', 'manifest': '捆綁構建清單', 'work': '工作中路徑'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
