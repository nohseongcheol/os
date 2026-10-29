#!/usr/bin/env python3
"""기존 路徑 호환 條目分. 實際資料 實現: ../工具集/構建用戶空間.py"""
import importlib as 取用值
import sys as 運行系統值
from pathlib import Path as 路徑
運行系統值.path.insert(0, str(路徑(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 運行器
    運行器.run_module('構建用戶空間', run_name='__main__', alter_sys=True)
else:
    實現 = 取用值.import_module('構建用戶空間')
    映射值 = {'mode': '方法模式', 'header': '標頭值', 'i': '序數索引', 'build_ccompiler': '創建C編譯器', 'ar': '存檔工具', 'posix': 'POSIX', 'payload': '載荷數據資料', 'flags': '配置項位元列', 'cases': '測試情況', 'cc': 'C編譯器', 'data': '資料', 'build_java_library': '創建Java庫', 'ld': '鏈接器工具', 'repo': '代碼庫路徑', 'build_python': '創建Python', 'inc': '包含路徑', 'argument': '已轉發值', 'text': '文本', 'headers': '標頭列表', 'cxx': 'Cpp編譯器', 'valid': '有效', 'build': '構建', 'build_users': '創建用戶空間', 'compiler': '編譯器工具', 'uzlib': '解壓庫', 'extra': '附加區域', 'phoff': '程式標頭偏移', 'offset': '偏移值', 'text_address': '命令地址', 'abi': '呼叫ABI', 'assembly': '彙編', 'run': '執行命令', 'path': '路徑', 'p': '資料位置', 'changed': '已更改', 'n': '項目個數', 'flag': '設置值', 'index': '查找索引', 'classes': '類別路徑', 'output': '輸出結果', 'loads': '載入項', 'data_address': '資料地址', 'symbol': '符號值', 'root': '根地址', 'patches': '修改列', 'source': '原始資料', 'sizes': '大小列', 'blobs': '二進制塊集', 'name': '名稱', 'value': '值', 'fmt': '資料格式', 'work': '工作中路徑'}
    for 上一個項目, 當前項目 in 映射值.items():
        if hasattr(實現, 當前項目): globals()[上一個項目] = getattr(實現, 當前項目)
