#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/構建C編譯器.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('構建C編譯器', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('構建C編譯器')
    映射值 = {'out': '結果資料', 'builtins': '內建項集', 'header': '標頭值', 'sdk': '開發工具套件', 'build_ccompiler': '創建C編譯器', 'i': '序數索引', 'elf': '可執行文件檔案', 'run': '執行命令', 'flags': '配置項位元列', 'path': '路徑', 'p': '資料位置', 'cc': 'C編譯器', 'obj': '目的地址檔案', 'flag': '設置值', 'ld': '鏈接器工具', 'objects': '目的地址檔案集', 'repo': '代碼庫路徑', 'v': '臨時資料', 'upstream': '上游', 'root': '根地址', 'assets': '資源素材', 'source': '原始資料', 'name': '名稱', 'includes': '包含項'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
