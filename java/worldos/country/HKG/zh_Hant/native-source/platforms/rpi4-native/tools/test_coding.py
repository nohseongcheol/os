#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/測試編碼方式.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('測試編碼方式', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('測試編碼方式')
    映射值 = {'out': '結果資料', 'expected': '預期', 'sdk': '開發工具套件', 'suffix': '後綴值', 'arc': '已壓縮捆綁', 'main': '運行', 'elf': '可執行文件檔案', 'run': '執行命令', 'name': '名稱', 'path': '路徑', 'p': '資料位置', 'ROOT': '項目根', 'report': '有效性驗證報告', 'args': '實際參數陣列'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
