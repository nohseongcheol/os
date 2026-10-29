#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. 宿主 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from 執行命令 import 命令


def 運行():
    參數解析器 = argparse.ArgumentParser(description=__doc__)
    參數解析器.add_argument('file', type=Path)
    參數解析器.add_argument('arguments', nargs='*')
    參數解析器.add_argument('--class-name', help='패키지가 있는 .class의 전체 名稱(예: 有效性校驗.測試捆綁)')
    參數解析器.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 調用 ABI 使用值')
    參數解析器.add_argument('--vnc', help='예: 127.0.0.1:2')
    參數解析器.add_argument('--include', action='append', type=Path, default=[], help='追加條目 class 檔案 또는 class 디렉터리(패키지 名稱 保持值)')
    實際參數陣列 = 參數解析器.parse_args()
    資料 = 實際參數陣列.file.read_bytes()
    if 實際參數陣列.class_name and 實際參數陣列.file.suffix != '.class': 參數解析器.error('--class-name은 .class 입력에서 사용합니다.')
    名稱 = 實際參數陣列.class_name + '.class' if 實際參數陣列.class_name else 實際參數陣列.file.name
    if len(資料) > 16384 or not 1 <= len(名稱.encode('utf-8')) <= 63 or '\n' in 名稱 or '\r' in 名稱:
        參數解析器.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    分類值 = '.elf' if 資料[:4] == b'\x7fELF' else 實際參數陣列.file.suffix
    if 實際參數陣列.linux and 分類值 != '.elf': 參數解析器.error('--linux는 ELF 바이너리에만 사용합니다.')
    if 分類值 not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        參數解析器.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(實際參數陣列.arguments) > 7 or any(len(字符串資料.encode('utf-8')) > 255 or '\n' in 字符串資料 or '\r' in 字符串資料 for 字符串資料 in 實際參數陣列.arguments):
        參數解析器.error('인수는 最大值 7개, 각각 UTF-8 255바이트 이하입니다.')
    選擇項集 = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if 實際參數陣列.vnc: 選擇項集 += ['-vnc', 實際參數陣列.vnc]
    程序 = subprocess.Popen(命令() + 選擇項集, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    就緒選擇器 = selectors.DefaultSelector(); 就緒選擇器.register(程序.stdout, selectors.EVENT_READ)
    def 接收消息(標記, 執行狀態超時=45):
        輸出結果 = bytearray(); 結束偏移 = time.monotonic() + 執行狀態超時
        while 標記 not in 輸出結果:
            if time.monotonic() > 結束偏移: raise RuntimeError('UART timeout: ' + 輸出結果.decode('utf-8', 'replace'))
            for 已按下值, _ in 就緒選擇器.select(0.1):
                片段值 = 已按下值.fileobj.read(4096)
                if 片段值: 輸出結果.extend(片段值)
            if b'PANIC:' in 輸出結果 or b'FAIL ' in 輸出結果: raise RuntimeError(輸出結果.decode('utf-8', 'replace'))
            if 程序.poll() is not None: raise RuntimeError('QEMU exited: ' + 輸出結果.decode('utf-8', 'replace'))
        return bytes(輸出結果)
    def 發送(行, 標記=b'jkoros-native> '):
        程序.stdin.write(行.encode('utf-8') + b'\n'); 程序.stdin.flush()
        return 接收消息(標記)
    def 執行命令(行):
        輸出結果 = 發送(行); sys.stdout.buffer.write(輸出結果); sys.stdout.buffer.flush()
        是否相等 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 輸出結果)
        if not 是否相等: raise RuntimeError('guest did not report exit status')
        return int(是否相等.group(1))
    try:
        接收消息(b'jkoros-native> ')
        檔案列表 = []
        for 包含條目 in 實際參數陣列.include:
            if 包含條目.is_dir():
                檔案列表 += [(str(資料位置.relative_to(包含條目).with_suffix('')).replace('/', '.') + '.class', 資料位置.read_bytes()) for 資料位置 in sorted(包含條目.rglob('*.class'))]
            else:
                檔案列表.append((包含條目.name, 包含條目.read_bytes()))
        檔案列表 = [(項目個數, 目的地址資料) for 項目個數, 目的地址資料 in 檔案列表 if 項目個數 != 名稱] + [(名稱, 資料)]
        for 上傳名稱, 上傳資料 in 檔案列表:
            if len(上傳資料) > 16384 or len(上傳名稱.encode('utf-8')) > 63 or '\n' in 上傳名稱 or '\r' in 上傳名稱:
                raise ValueError('追加條目 파일의 名稱/大小 限制值 초과: ' + 上傳名稱)
            發送('load ' + shlex.quote(上傳名稱), b'hex> ')
            for 序數索引 in range(0, len(上傳資料), 64): 發送(上傳資料[序數索引:序數索引+64].hex(), b'hex> ')
            if b'LOADED' not in 發送('.'): raise RuntimeError('upload failed: ' + 上傳名稱)
            已轉儲 = 發送('hex ' + shlex.quote(上傳名稱))
            是否相等 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 已轉儲, re.S)
            if not 是否相等 or bytes.fromhex(''.join(是否相等.group(2).decode().split())) != 上傳資料: raise RuntimeError('upload verification failed')
        if 分類值 == '.java' and 執行命令('javac ' + shlex.quote(名稱)) != 0: return 1
        可執行文件映像 = 實際參數陣列.file.stem + '.elf'
        if 分類值 == '.c' and 執行命令('cc ' + shlex.quote(名稱) + ' -o ' + shlex.quote(可執行文件映像)) != 0: return 1
        執行條目 = 'java ' + shlex.quote(實際參數陣列.class_name or 實際參數陣列.file.stem) if 分類值 in ('.java', '.class') else ('python ' if 分類值 == '.py' else 'run ') + shlex.quote(名稱)
        if 分類值 == '.jar': 執行條目 = 'java -jar ' + shlex.quote(名稱)
        if 分類值 == '.c': 執行條目 = 'run ' + shlex.quote(可執行文件映像)
        if 實際參數陣列.linux: 執行條目 = 'run --linux ' + shlex.quote(名稱)
        if 實際參數陣列.arguments: 執行條目 += ' ' + ' '.join(shlex.quote(字符串資料) for 字符串資料 in 實際參數陣列.arguments)
        return 0 if 執行命令(執行條目) == 0 else 1
    finally:
        if 程序.poll() is None:
            程序.terminate()
            try: 程序.wait(timeout=5)
            except subprocess.TimeoutExpired: 程序.kill(); 程序.wait(timeout=5)
        就緒選擇器.close(); 程序.stdin.close(); 程序.stdout.close()


if __name__ == '__main__':
    raise SystemExit(運行())
