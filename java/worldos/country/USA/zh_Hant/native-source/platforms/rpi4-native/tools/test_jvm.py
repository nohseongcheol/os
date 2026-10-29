#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/測試JVM.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('測試JVM', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('測試JVM')
    映射值 = {'message': '通知文本', 's': '字符串資料', 'actual': '實際結果', 'match': '是否相等', 'payload': '載荷數據資料', 'cases': '測試情況', 'fixture': '測試資料', 'main': '運行', 'ROOT': '項目根', 'text': '文本', 'valid': '有效', 'includes': '包含項', 'include': '包含條目', 'expected': '預期', 'sources': '原始碼列表', 'tmp': '臨時路徑', 'done': '已完成總量', 'classes': '類別路徑', 'output': '輸出結果', 'result': '結果', 'cmd': '命令參數列', 'name': '名稱', 'jar': 'Java捆綁', 'report': '有效性驗證報告', 'tests': '測試列表'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
