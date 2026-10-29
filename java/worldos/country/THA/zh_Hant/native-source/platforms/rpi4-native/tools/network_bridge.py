#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/網路橋接.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('網路橋接', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('網路橋接')
    映射值 = {'response': '響應', 'parts': '路徑組件', 's': '字符串資料', 'i': '序數索引', 'close': '關閉', 'forward': '轉發中規則', 'slip_input': '串行線路_Internet_協議輸入', 'self': '自身值', 'item': '條目值', 'flags': '配置項位元列', 'ftp_port': '檔案傳送埠編號', 'args': '實際參數陣列', 'server': '服務器值', 'data': '資料', 'ethernet_input': '以太網輸入', 'trace_packet': '追蹤數據包', 'GATEWAY': '網關硬件地址', 'rule': '規則值', 'protocol': '網路ABI', 'forwards': '轉發中規則列', 'occupied': '已佔用', 'host': '宿主', 'ack': '確認狀態編號', 'serial_port': '串行埠編號', 'readers': '讀取器集', 'guest': '客戶機', 'destination': '目的地址資料地址', 'ethernet_port': '以太網埠', 'b': '第二值', 'MAC': '計算機地址', 'arp': '地址分辨率數據包', 'writable': '可寫', 'direction': '方向', 'seq': '排序編號', 'frame': '執行狀態幀', 'loop': '週期值', 'port': '埠編號', 'offset': '偏移值', 'readable': '能夠讀取', 'c': '字元程式碼', 'p': '資料位置', 'writers': '寫入器集', 'IP': '互聯網地址值', 'e': '輔助條目', 'n': '項目個數', 'packet': '數據包資料', 'arguments': '已轉發實際參數', 'source': '原始資料', 'NetworkBridge': '網路橋接', 'window': '窗口', 'capture': '捕獲'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
