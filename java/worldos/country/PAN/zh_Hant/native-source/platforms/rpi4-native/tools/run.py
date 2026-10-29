#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/執行命令.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('執行命令', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('執行命令')
    映射值 = {'supported': '支持功能列', 'parser': '參數解析器', 'qemu': '測試替身計算機', 'run_desktop': '運行桌面', 'main': '運行', 'host': '宿主', 'status': '狀態值', 'NetworkBridge': '網路橋接', 'ROOT': '項目根', 'bridge': '橋接', 'loader': '加載器', 'base': '背景值', 'options': '選擇項集', 'binary': '二進制', 'args': '實際參數陣列', 'command': '命令'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
