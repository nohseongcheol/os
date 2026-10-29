#!/usr/bin/env python3
"""上一個項目 Python 경로를 Java 미리 번역기에 연결한다. 翻譯原始碼 구현은 Java工具/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 編譯器 import 編譯過程錯誤

項目根 = Path(__file__).resolve().parent

class 計算機程式碼編譯器:
    def __init__(自身值, 輸入類別集, 執行狀態目標='kernel', 堆機器字個數=262144):
        自身值.路徑列表 = [資料.路徑 for 資料 in 輸入類別集]
        自身值.執行狀態目標 = 執行狀態目標
        自身值.堆機器字個數 = 堆機器字個數

    def 生成(自身值, 條目分, 導出條目列, 通用字元表示法=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 任務:
            結果路徑 = Path(任務)/'generated.c'
            命令 = ['sh', str(項目根/'提前所屬時間.sh'), '--entry', 條目分,
                    '--profile', 自身值.執行狀態目標, '--heap-words', str(自身值.堆機器字個數), '-o', str(結果路徑)]
            if 通用字元表示法: 命令.append('--ucn')
            for 賦值值 in 導出條目列: 命令.extend(['--export', 賦值值])
            命令.extend(str(路徑) for 路徑 in 自身值.路徑列表)
            結果 = subprocess.run(命令, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if 結果.returncode: raise 編譯過程錯誤(結果.stderr.decode('utf-8', 'replace'))
            return 結果路徑.read_text()

def 運行():
    raise SystemExit(subprocess.call(['sh', str(項目根/'提前所屬時間.sh')] + sys.argv[1:]))

if __name__ == '__main__': 運行()
