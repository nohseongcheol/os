#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/測試桌面.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('測試桌面', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('測試桌面')
    映射值 = {'x': '橫座標座標', 'typing': '已輸入字元', 'message': '通知文本', 'start': '運行', 'down': '是否按下中', 'exact': '精確值', 'i': '序數索引', 'press': '按下鍵', 'rectangles': '矩形列列表', 'sym': '符號', 'j': '內部側序數', 'deadline': '截止時間時間', 'proc': '程序', 'data': '資料', 'main': '運行', 'w': '已請求寬度值', 'init': '初始值', 'block': '資料塊', 'ROOT': '項目根', 'text': '文本', 'marker': '標記', 'report': '有效性驗證報告', 'until': '直到', 'clipboard': '剪貼板值', 'dst': '目的地址地址', 'seen': '已看見條目列', 'poll': '就緒情況監視器', 'transcript': '執行記錄', 'port': '埠編號', 'offset': '偏移值', 'h': '已請求高度值', 'src': '原始地址', 'event': '事件', 'encoding': '字元設定', 'size': '大小', 'key': '已按下值', 'pixels': '像素列列表', 'y': 'Y_按鈕座標', 'output': '輸出結果', 'symbol': '符號值', 'client': '客戶端', 'char': '字元資料', 'rgb': '紅_綠_藍顏色'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
