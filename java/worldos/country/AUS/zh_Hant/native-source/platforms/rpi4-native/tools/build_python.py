#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/構建Python.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('構建Python', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('構建Python')
    映射值 = {'ld': '鏈接器工具', 'archive': '存檔', 'SHA256': '有效性驗證哈希', 'build_python': '創建Python', 'root': '根地址', 'source': '原始資料', 'name': '名稱', 'path': '路徑', 'VERSION': '版本版次值', 'cc': 'C編譯器', 'tar': 'TAR捆綁', 'newlib': 'Newlib包含路徑', 'member': '成員'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
