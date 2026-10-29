#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/構建網路.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('構建網路', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('構建網路')
    映射值 = {'obj': '目的地址檔案', 'objects': '目的地址檔案集', 'library': '庫', 'output': '輸出結果', 'port': '埠編號', 'root': '根地址', 'files': '檔案列表', 'source': '原始資料', 'run': '執行命令', 'flags': '配置項位元列', 'path': '路徑', 'build_network': '創建網路', 'cc': 'C編譯器', 'ar': '存檔工具'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
