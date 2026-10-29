#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/測試Remmina.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('測試Remmina', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('測試Remmina')
    映射值 = {'wait': '等待', 'typing': '已輸入字元', 'start': '運行', 'profile': '配置檔', 'focused': '已聚焦', 'serial': '串行輸入輸出', 'keys': '已按下鍵列', 'server': '服務器值', 'log': '日誌記錄', 'args': '實際參數陣列', 'deadline': '截止時間時間', 'data': '資料', 'candidate': '候選', 'logs': '日誌記錄列', 'kw': '已命名實際參數', 'number': '數值值', 'main': '運行', 'ready': '準備狀態完成', 'found': '搜索結果', 'guest': '客戶機', 'ROOT': '項目根', 'marker': '標記', 'text': '文本', 'out': '結果資料', 'env': '環境', 'f': '檔案條目', 'port': '埠編號', 'offset': '偏移值', 'version': '版本編號', 'p': '資料位置', 'selector': '就緒選擇器', 'xvfb': '虛擬顯示操作', 'display': '顯示操作設備', 'n': '項目個數', 'key': '已按下值', 'processes': '運行中程序列', 'rootfs': '根文件系統', 'xdo': '虛擬輸入工具', 'name': '名稱', 'window': '窗口', 'report': '有效性驗證報告', 'work': '工作中路徑'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
