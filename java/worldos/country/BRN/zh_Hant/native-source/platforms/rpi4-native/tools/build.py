#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/構建系統.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('構建系統', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('構建系統')
    映射值 = {'network': '使用網路', 'BUILD': '構建路徑', 'ar': '存檔工具', 'build_examples': '創建範例集', 'posix': 'POSIX', 'font_data': '字體資料', 'flags': '配置項位元列', 'a': '首位值', 'cc': 'C編譯器', 'args': '實際參數陣列', 'source_flags': '原始配置項', 'ld': '鏈接器工具', 'method': '方法條目', 'main': '運行', 'objcopy': '物件檔案轉換器', 'ROOT': '項目根', 'cxx': 'Cpp編譯器', 'includes': '包含項', 'compiler': '編譯器工具', 'build_users': '創建用戶空間', 'f': '檔案條目', 'extra': '附加區域', 'exports': '導出表', 'jobs': '構建作業列', 'run': '執行命令', 'path': '路徑', 'REPO': '代碼庫根', 'tool': '工具集', 'classes': '類別路徑', 'output': '輸出結果', 'samples': '範例條目列', 'symbol': '符號值', 'source': '原始資料', 'name': '名稱', 'build_network': '創建網路', 'font_info': '字體信息', 'manifest': '捆綁構建清單', 'work': '工作中路徑'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
