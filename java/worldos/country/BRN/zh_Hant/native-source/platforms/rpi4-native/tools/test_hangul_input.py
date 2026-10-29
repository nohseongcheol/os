#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/測試韓文字母輸入.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('測試韓文字母輸入', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('測試韓文字母輸入')
    映射值 = {'expected': '預期', 'Keyboard': '鍵盤', 'press': '按下鍵', 'self': '自身值', 'test_modes_repeat_and_commit': '測試模式列重複與提交', 'keys': '已按下鍵列', 'test_paste_and_unicode': '測試粘貼與Unicode', 'data': '資料', 'key': '已按下值', 'send': '發送', 'test_words': '測試單詞列', 'InputTests': '測試韓文字母輸入', 'test_backspace': '測試退格', 'symbol': '符號值', 'char': '字元資料', 'type': '類型分類'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
