#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/測試範例集.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('測試範例集', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('測試範例集')
    映射值 = {'count': '條目個數', 'exact': '精確值', 'expected_file': '預期檔案', 'ftp_port': '檔案傳送埠編號', 'data': '資料', 'graphics_command': '圖形命令', 'main': '運行', 'row': '列位置', 'init': '初始值', 'target': '目標值', 'ROOT': '項目根', 'text': '文本', 'binary': '二進制', 'out': '結果資料', 'entry': '條目分', 'got': '已接收個數', 'port': '埠編號', 'graphics_start': '開始繪圖', 'col': '欄位置', 'begin': '開始偏移', 'kind': '分類值', 'selector': '就緒選擇器', 'n': '項目個數', 'key': '已按下值', 'y': 'Y_按鈕座標', 'client': '客戶端', 'line': '行', 'report': '有效性驗證報告', 'language': '語言', 'x': '橫座標座標', 'start': '運行', 'rgb': '紅_綠_藍顏色', 'down': '是否按下中', 'listing': '發送列表', 'payload': '載荷數據資料', 'proc': '程序', 'w': '已請求寬度值', 'temporary': '臨時', 'echo': '回顯服務器條目', 'label': '名稱表', 'content': '內容值', 'argument': '已轉發值', 'EchoServers': '回顯服務器列', 'marker': '標記', 'expected': '預期', 'test_language': '測試語言', 'filename': '檔案條目名稱', 'shell': '命令殼', 'color': '像素顏色', 'transcript': '執行記錄', 'offset': '偏移值', 'h': '已請求高度值', 'run': '執行命令', 'c': '字元程式碼', 'path': '路徑', 'encoding': '字元設定', 'end': '結束偏移', 'ftp': '檔案傳送連接狀態', 'pixels': '像素列列表', 'symbol': '符號值', 'source': '原始資料', 'name': '名稱', 'receive': '接收消息', 'manifest': '捆綁構建清單'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
