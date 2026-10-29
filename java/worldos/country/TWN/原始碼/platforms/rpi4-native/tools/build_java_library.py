#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/構建Java庫.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('構建Java庫', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('構建Java庫')
    映射值 = {'header': '標頭值', 'sources': '原始碼列表', 'i': '序數索引', 'info': '系統信息', 'payload': '載荷數據資料', 'src': '原始地址', 'run': '執行命令', 'build_java_library': '創建Java庫', 'relative': '相對路徑', 'classes': '類別路徑', 'dist': '分發路徑', 'archive': '存檔', 'output': '輸出結果', 'root': '根地址', 'name': '名稱', 'jar': 'Java捆綁', 'b': '第二值', 'entries': '條目列列表'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
