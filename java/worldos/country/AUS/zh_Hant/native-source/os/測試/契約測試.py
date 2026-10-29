#!/usr/bin/env python3
"""宿主 libc 없이 연결한 中文 C 프로그램을 實際資料 ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 測試用戶網路 import 虛擬機器

位置 = Path(__file__).resolve().parents[1]

def 執行命令():
    結果 = {}
    服務器值 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    服務器值.bind(('127.0.0.1', 0))
    服務器值.settimeout(0.1)
    埠編號 = 服務器值.getsockname()[1]
    已接收資料 = []
    終止狀態狀態 = threading.Event()
    def 回顯回覆():
        while not 終止狀態狀態.is_set():
            try:
                資料, 地址 = 服務器值.recvfrom(4096)
            except socket.timeout:
                continue
            已接收資料.append(資料)
            服務器值.sendto(資料, 地址)
    後臺任務值 = threading.Thread(target=回顯回覆, daemon=True)
    後臺任務值.start()
    try:
        for 種類值 in ('elf', 'iso'):
            計算機 = 虛擬機器(位置 / ('build/kernel.' + 種類值), 種類值)
            try:
                for 迭代值 in range(2):
                    計算機.命令('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    計算機.命令('run posixudp ' + str(埠編號), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                運行 = len(計算機.日誌記錄)
                計算機.串行值.sendall(b'run posixinput\n')
                計算機.等待狀態狀態('POSIX INPUT READY', 運行)
                計算機.串行值.sendall(b'abcdef')
                輸出 = 計算機.等待狀態狀態('jkoros> ', 運行)
                assert 'POSIX INPUT PASS' in 輸出 and 'Exit: 0' in 輸出, 輸出
                計算機.命令('javac Hello.java', ['Exit: 0'])
                計算機.命令('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                計算機.命令('run hello recovered', ['arg: recovered', 'Exit: 0'])
                結果[種類值] = 計算機.日誌記錄.decode('utf-8', 'replace')
                print('PASS:', 種類值, 'POSIX 檔案/공유 位置/삭제 수명/地址 保護值/UDP/표준 輸入值/기존 Java', flush=True)
            finally:
                計算機.關閉()
        assert b'posix-udp' in 已接收資料 and b'truncate' in 已接收資料 and b'' in 已接收資料
    finally:
        終止狀態狀態.set(); 後臺任務值.join(timeout=2); 服務器值.close()
    結果['host_datagrams'] = [資料.decode() for 資料 in 已接收資料]
    (位置 / 'build/契約測試.json').write_text(json.dumps(結果, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    執行命令()
