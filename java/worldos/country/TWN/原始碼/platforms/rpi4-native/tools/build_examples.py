#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/構建範例集.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('構建範例集', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('構建範例集')
    映射值 = {'out': '結果資料', 'build_examples': '創建範例集', 'files': '檔案列表', 'java': '執行Java', 'run': '執行命令', 'path': '路徑', 'p': '資料位置', 'readme': '自述文件', 'build_java_library': '創建Java庫', 'code': '指令序列', 'index': '查找索引', 'classes': '類別路徑', 'repo': '代碼庫路徑', 'root': '根地址', 'content': '內容值', 'source': '原始資料', 'name': '名稱', 'target': '目標值', 'manifest': '捆綁構建清單', 'language': '語言'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
