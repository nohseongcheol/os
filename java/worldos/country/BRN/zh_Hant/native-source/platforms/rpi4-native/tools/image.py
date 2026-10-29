#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/創建映像.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('創建映像', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('創建映像')
    映射值 = {'total': '總計容量', 'start': '運行', 'firmware': '固件值', 'files': '檔案列表', 'archive_base': '存檔基底', 'partition': '分區檔案', 'archive': '存檔', 'main': '運行', 'block': '資料塊', 'ROOT': '項目根', 'boot': '啓動路徑', 'stage': '階段值', 'out': '結果資料', 'expected': '預期', 'f': '檔案條目', 'src': '原始地址', 'path': '路徑', 'p': '資料位置', 'extracted': '已提取', 'member': '成員', 'mbr': '主控啓動記錄', 'image': '映像', 'sector_count': '扇區個數', 'dist': '分發路徑', 'sha': '計算哈希', 'license_': '許可', 'source': '原始資料', 'name': '名稱', 'value': '值', 'manifest': '捆綁構建清單', 'dest': '目的地址值位置', 'work': '工作中路徑'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
