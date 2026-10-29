#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 測試用戶網路 import 虛擬機器, 位置
from Java測試 import 編輯值, 客戶機檔案

def 執行命令():
    結果 = {}
    原始碼 = (位置.parent / 'posix-kor/Java範例/FileDemo.java').read_text()
    for 種類值 in ('elf', 'iso'):
        計算機 = 虛擬機器(位置 / ('build/kernel.' + 種類值), 種類值, 網路值=False)
        try:
            編輯值(計算機, 'FileDemo.java', 原始碼)
            計算機.命令('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for 迭代值 in range(2):
                輸出 = 計算機.命令('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            條目列表 = 計算機.命令('ls', ['java.txt  3 bytes'])
            大小 = int(re.search(r'FileDemo.class\s+(\d+) bytes', 條目列表)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 臨時值:
                目錄值 = Path(臨時值)
                客戶機檔案(計算機, 2, 大小, 目錄值 / 'FileDemo.class')
                宿主 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(目錄值), 'FileDemo'], cwd=str(目錄值), universal_newlines=True)
                assert 宿主 == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', 宿主
                assert (目錄值 / 'java.txt').read_bytes() == b'A\xffB'
            編輯值(計算機, 'FileDemo.java', 原始碼.replace('output.write(65);', 'output.close(); output.write(65);'))
            計算機.命令('javac FileDemo.java', ['Exit: 0'])
            計算機.命令('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            編輯值(計算機, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            計算機.命令('javac FileDemo.java', ['Exit: 0'])
            計算機.命令('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            計算機.命令('run hello recovered', ['Exit: 0'])
            結果[種類值] = 計算機.日誌記錄.decode('utf-8', 'replace')
        finally:
            計算機.關閉()
        print('PASS:', 種類值, '게스트 Java 檔案 生成/追加繼續狀態/位元組值/EOF/是否已關閉/失敗值/OpenJDK 교차 執行命令', flush=True)
    (位置 / 'build/Java檔案測試.json').write_text(json.dumps(結果, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    執行命令()
