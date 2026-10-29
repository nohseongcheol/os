#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/執行檔案.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('執行檔案', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('執行檔案')
    映射值 = {'timeout': '執行狀態超時', 's': '字符串資料', 'i': '序數索引', 'match': '是否相等', 'files': '檔案列表', 'program': '執行條目', 'executable': '可執行文件映像', 'args': '實際參數陣列', 'chunk': '片段值', 'data': '資料', 'proc': '程序', 'send': '發送', 'main': '運行', 'marker': '標記', 'command': '命令', 'include': '包含條目', 'dumped': '已轉儲', 'run': '執行命令', 'p': '資料位置', 'parser': '參數解析器', 'options': '選擇項集', 'kind': '分類值', 'selector': '就緒選擇器', 'upload_data': '上傳資料', 'end': '結束偏移', 'n': '項目個數', 'd': '目的地址資料', 'key': '已按下值', 'output': '輸出結果', 'line': '行', 'name': '名稱', 'upload_name': '上傳名稱', 'receive': '接收消息'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
