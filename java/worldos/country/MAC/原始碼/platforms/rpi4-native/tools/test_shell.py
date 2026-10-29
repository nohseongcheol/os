#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/測試命令殼.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('測試命令殼', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('測試命令殼')
    映射值 = {'timeout': '執行狀態超時', 'x': '橫座標座標', 'msg': '網路消息', 'i': '序數索引', 'reply': '回覆', 'call': '調用', 'args': '實際參數陣列', 'chunk': '片段值', 'data': '資料', 'proc': '程序', 'long_text': '長整數文本', 'restored': '已恢復資料', 'send': '發送', 'file': '檔案', 'main': '運行', 'found': '搜索結果', 'ROOT': '項目根', 'text': '文本', 'marker': '標記', 'command': '命令', 'expected': '預期', 'pixel': '像素', 'shell': '命令殼', 'poll': '就緒情況監視器', 'transcript': '執行記錄', 'end': '結束偏移', 'image': '映像', 'key': '已按下值', 'y': 'Y_按鈕座標', 'output': '輸出結果', 'result': '結果', 'client': '客戶端', 'line': '行', 'stream': '流值', 'name': '名稱', 'value': '值', 'receive': '接收消息', 'report': '有效性驗證報告', 'work': '工作中路徑', 'qmp': '測試替身控制連接狀態'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
