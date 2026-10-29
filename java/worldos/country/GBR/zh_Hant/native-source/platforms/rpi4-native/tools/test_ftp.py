#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/測試FTP.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('測試FTP', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('測試FTP')
    映射值 = {'timeout': '執行狀態超時', 'payload': '載荷數據資料', 'broken': '已損壞', 'linux_example': 'Linux範例', 'chunk': '片段值', 'data': '資料', 'proc': '程序', 'code': '指令序列', 'linux': 'Linux檔案', 'archive': '存檔', 'main': '運行', 'net_source': '網路層原始碼', 'temporary': '臨時', 'static_source': '靜態原始碼', 'java_source': 'Java原始碼', 'echo': '回顯服務器條目', 'ROOT': '項目根', 'text': '文本', 'marker': '標記', 'EchoFixture': '回顯測試夾具', 'command': '命令', 'out': '結果資料', 'expected': '預期', 'server_source': '服務器原始碼', 'shell': '命令殼', 'upload': '上傳檔案集', 'transcript': '執行記錄', 'port': '埠編號', 'native': '原生', 'elf': '可執行文件檔案', 'server_udp_port': '服務器數據報埠', 'packed': '已打包', 'bridge': '橋接', 'selector': '就緒選擇器', 'end': '結束偏移', 'e': '輔助條目', 'ftp': '檔案傳送連接狀態', 'key': '已按下值', 'bytecode': '字節碼', 'peer': '對端值', 'result': '結果', 'unchanged': '已保留資料', 'line': '行', 'server_tcp_port': '服務器流埠', 'source': '原始資料', 'NetworkBridge': '網路橋接', 'jar': 'Java捆綁', 'receive': '接收消息', 'report': '有效性驗證報告'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
