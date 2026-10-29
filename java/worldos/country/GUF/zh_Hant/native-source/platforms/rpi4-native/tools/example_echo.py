#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/回顯示例服務器.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('回顯示例服務器', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('回顯示例服務器')
    映射值 = {'data': '資料', 'sock': '通訊端值', 'tcp_port': 'TCP埠', 'chunk': '片段值', 'received': '擁有已接收', 'self': '自身值', 'UDP': '數據報句柄申請', 'thread': '後臺任務', 'echo': '回顯服務器條目', 'TCP': '句柄連接狀態申請', 'EchoServers': '回顯服務器列', 'parser': '參數解析器', 'server': '服務器值', 'udp_port': 'UDP埠', 'args': '實際參數陣列'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
