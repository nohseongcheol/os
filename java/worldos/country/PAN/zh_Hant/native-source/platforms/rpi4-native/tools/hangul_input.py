#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/韓文字母輸入.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('韓文字母輸入', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('韓文字母輸入')
    映射值 = {'old': '上一個項目', 'backspace': '退格', 'committed': '已提交', 'KEYS': '鍵導航', 'self': '自身值', 'FINALS': '複合最終字母構件', 'VOWELS': '複合中聲字母構件', 'INITIAL': '初始字母構件表', 'initial': '初始字母構件', 'commit': '提交合成狀態', 'feed': '供給鍵', 'vowel': '中聲字母構件', 'Hangul': '合成韓文字母', 'SPLIT': '分割最終字母構件', 'final': '最終字母構件', 'key': '已按下值', 'send': '發送', 'left': '左側', 'FINAL': '最終字母構件表', 'history': '歷史記錄', 'pair': '一一對', 'char': '字元資料', 'VOWEL': '中聲字母構件表', 'right': '右', 'value': '值', 'text': '文本'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
