#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/SDK編譯.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('SDK編譯', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('SDK編譯')
    映射值 = {'compiler': '編譯器工具', 'obj': '目的地址檔案', 'sdk': '開發工具套件', 'output': '輸出結果', 'main': '運行', 'elf': '可執行文件檔案', 'is_c': '是否C語言', 'parser': '參數解析器', 'language': '語言', 'work': '工作中路徑', 'args': '實際參數陣列'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
