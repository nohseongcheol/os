#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/構建終端字體.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('構建終端字體', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('構建終端字體')
    映射值 = {'data': '資料', 'img': '繪圖', 'bits': '位元列列表', 'x': '橫座標座標', 'draw': '繪製屏幕', 'licences': '許可列', 'paths': '路徑列表', 'y': 'Y_按鈕座標', 'main': '運行', 'src': '原始地址', 'fonts': '字體列表', 'ROOT': '項目根', 'p': '資料位置', 'cp': '字元編碼狀態', 'target': '目標值'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
