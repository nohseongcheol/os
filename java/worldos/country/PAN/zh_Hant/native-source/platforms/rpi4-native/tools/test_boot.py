#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/啓動測試.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('啓動測試', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('啓動測試')
    映射值 = {'timeout': '執行狀態超時', 'response': '響應', 'msg': '網路消息', 'exact': '精確值', 'markers': '標記列', 'i': '序數索引', 'match': '是否相等', 'execute': '執行任務', 'cancel': '取消操作', 'cmd_byte': '命令位元組', 'reply': '回覆', 'points': '點列', 'server': '服務器值', 'data': '資料', 'prompt': '提示', 'enter': '進入', 'imported': '已導入', 'send': '發送', 'main': '運行', 'ROOT': '項目根', 'text': '文本', 'first_gui': '首位GUI', 'pixel': '像素', 'java_class': 'Java類別', 'upload': '上傳檔案集', 'pixels_file': '像素檔案', 'pixels_data': '像素資料', 'edit': '編輯值', 'receive_until': '接收直到', 'selector': '就緒選擇器', 'size': '大小', 'qmp_path': 'QMP路徑', 'key': '已按下值', 'second_gui': '第二GUI', 'y': 'Y_按鈕座標', 'result': '結果', 'samples': '範例條目列', 'client': '客戶端', 'line': '行', 'report': '有效性驗證報告', 'work': '工作中路徑', 'x': '橫座標座標', 'python_checks': 'Python檢查項', 'download': '下載', 'greeting': '問候例', 'dims': '尺寸值', 'chunk': '片段值', 'deadline': '截止時間時間', 'proc': '程序', 'content': '內容值', 'block': '資料塊', 'marker': '標記', 'command': '命令', 'expected': '預期', 'shell': '命令殼', 'drawing': '繪圖路徑', 'f': '檔案條目', 'transcript': '執行記錄', 'offset': '偏移值', 'path': '路徑', 'screenshot': '屏幕剪輯', 'arguments': '已轉發實際參數', 'pixels': '像素列列表', 'viewer': '屏幕客戶端', 'output': '輸出結果', 'stream': '流值', 'cmd': '命令參數列', 'name': '名稱', 'qmp': '測試替身控制連接狀態'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
