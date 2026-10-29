#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/桌面視圖.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('桌面視圖', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('桌面視圖')
    映射值 = {'count': '條目個數', 'special': '特殊鍵', 'error': '錯誤', 'exact': '精確值', 'network': '使用網路', 'closed': '是否已關閉', 'length': '長度', 'opened': '已打開', 'ftp_port': '檔案傳送埠編號', 'server': '服務器值', 'resources': '資源集', 'data': '資料', 'shift': '移位鍵', 'send': '發送', 'run_desktop': '運行桌面', 'protocol': '網路ABI', 'forwards': '轉發中規則列', 'host': '宿主', 'text': '文本', 'korean': '韓語', 'port': '埠編號', 'signum': '信號編號', 'version': '版本編號', 'parser': '參數解析器', 'bridge': '橋接', 'kind': '分類值', 'tail': '結尾部分', 'size': '大小', 'previous_buttons': '上一個按鈕列', 'key': '已按下值', 'y': 'Y_按鈕座標', 'prefix': '前導部分', 'client': '客戶端', 'char': '字元資料', 'work': '工作中路徑', 'Keyboard': '鍵盤', 'x': '橫座標座標', 'down': '是否按下中', 'net': '網路橋接條目', 'self': '自身值', 'mode_changed': '模式已更改', 'serial': '串行輸入輸出', 'args': '實際參數陣列', 'Hangul': '合成韓文字母', 'chunk': '片段值', 'proc': '程序', 'Desktop': '連接桌面', 'buttons': '按鈕列', 'thread': '後臺任務', 'pressed': '是否已按下', 'previous': '上一個', 'toggle': '切換模式', 'command': '命令', 'sock': '通訊端值', 'frame': '執行狀態幀', 'ctrl': '控制鍵', 'path': '路徑', 'cp': '字元編碼狀態', 'terminate': '終止', 'security': '安全性', 'vnc_port': 'VNC埠', 'body': '主體文本', 'index': '查找索引', 'exited': '擁有已退出', 'keysym': '鍵符號', 'output': '輸出結果', 'keyboard': '鍵盤條目', 'interrupted': '已中斷', 'listener': '接收埠', 'reader': '讀取器', 'NetworkBridge': '網路橋接', 'gui': '繪圖屏幕', 'worker': '處理任務'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
