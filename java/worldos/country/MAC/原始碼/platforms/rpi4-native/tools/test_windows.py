#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/測試窗口列.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('測試窗口列', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('測試窗口列')
    映射值 = {'wait': '等待', 'x': '橫座標座標', 's': '字符串資料', 'xy': '座標一對', 'sel': '選擇器', 'seconds': '秒數單位', 'log': '日誌記錄', 'at': '當前位置', 'send': '發送', 'main': '運行', 'req': '申請值', 'hot': '快捷操作值', 'pump': '句柄事件', 'ROOT': '項目根', 'marker': '標記', 'b': '第二值', 'command': '命令', 'shell': '命令殼', 'f': '檔案條目', 'color': '像素顏色', 'click': '單擊按鈕', 'k': '第三索引', 'c': '字元程式碼', 'r': '已返回值', 'p': '資料位置', 'done': '已完成總量', 'end': '結束偏移', 'command_mode': '命令模式', 'key': '已按下值', 'y': 'Y_按鈕座標', 'pixels': '像素列列表', 'result': '結果', 'report': '有效性驗證報告', 'dest': '目的地址值位置', 'work': '工作中路徑', 'qmp': '測試替身控制連接狀態'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
