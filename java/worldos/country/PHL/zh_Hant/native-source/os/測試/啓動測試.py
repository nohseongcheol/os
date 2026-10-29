#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 串行值/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

位置 = Path(__file__).resolve().parents[1]


def 等待(檢查項, 說明, 限制值=15):
    結尾 = time.monotonic() + 限制值
    while time.monotonic() < 結尾:
        結果 = 檢查項()
        if 結果:
            return 結果
        time.sleep(0.05)
    raise AssertionError('時間值 초과: ' + 說明)


def 測試(種類值):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 臨時值:
        臨時值 = Path(臨時值)
        串行路徑 = 臨時值 / 'serial.sock'
        監視器路徑 = 臨時值 / 'monitor.sock'
        命令 = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(串行路徑) + ',server,nowait',
                '-monitor', 'unix:' + str(監視器路徑) + ',server,nowait']
        命令 += ['-kernel', str(位置 / 'build/kernel.elf')] if 種類值 == 'elf' else [
            '-cdrom', str(位置 / 'build/kernel.iso'), '-boot', 'd']
        # 串行值 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        命令 += ['-S']
        程序值 = subprocess.Popen(命令, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        串行值 = socket.socket(socket.AF_UNIX)
        監視器值 = socket.socket(socket.AF_UNIX)
        日誌記錄 = bytearray()
        try:
            def 準備通訊端():
                if 程序值.poll() is not None:
                    raise AssertionError(程序值.stderr.read().decode('utf-8', 'replace'))
                return 串行路徑.exists() and 監視器路徑.exists()
            等待(準備通訊端, 'QEMU 通訊端值')
            串行值.connect(str(串行路徑))
            監視器值.connect(str(監視器路徑))
            串行值.setblocking(False)
            監視器值.sendall(b'cont\n')

            def 頭文件(字符串, 運行=0):
                讀取, _, _ = select.select([串行值], [], [], 0.1)
                if 讀取:
                    資料 = 串行值.recv(65536)
                    if not 資料:
                        raise AssertionError('串行值 連接 退出程式')
                    日誌記錄.extend(資料)
                if 程序值.poll() is not None:
                    raise AssertionError('QEMU 비정상 退出程式: ' + str(程序值.returncode))
                return 字符串.encode('utf-8') in 日誌記錄[運行:]

            def 測試命令列(輸入值, 期望狀態):
                運行 = len(日誌記錄)
                串行值.sendall(輸入值.encode('ascii'))
                等待(lambda: 頭文件(期望狀態, 運行), 期望狀態)
                等待(lambda: 頭文件('jkoros> ', 運行), '命令 之後狀態 프롬프트')

            等待(lambda: 頭文件('READY'), 種類值 + ' 啓動')
            assert b'JAVA SELFTEST PASS' in 日誌記錄
            assert 'Java 기계어 內核值 運行'.encode() in 日誌記錄
            測試命令列('info\r\n', 'embedded subset JVM / polling kernel')
            測試命令列('help\n', 'free N | echo TEXT')
            測試命令列('mem\n', ' / 8 (각 4096바이트)')
            測試命令列('echo natix\bve\n', 'native\r\n')
            for 編號 in range(8):
                測試命令列('alloc\n', '區段值 編號: ' + str(編號))
            測試命令列('alloc\n', '區段值 編號: -1')
            測試命令列('free 3\n', '반환됨')
            測試命令列('free 3\n', '할당되지 않은 區段值')
            測試命令列('free 99\n', '사용법: free 0..7')
            測試命令列('alloc\n', '區段值 編號: 3')
            測試命令列('free 0\n', '반환됨')
            測試命令列('test\n', 'JAVA SELFTEST PASS')
            測試命令列('unknown\n', '알 數 없는 명령입니다')
            測試命令列('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            運行 = len(日誌記錄)
            for 鍵值 in ('i', 'n', 'f', 'o', 'ret'):
                監視器值.sendall(('sendkey ' + 鍵值 + ' 30\n').encode())
                time.sleep(0.09)
            等待(lambda: 頭文件('embedded subset JVM / polling kernel', 運行), 'PS/2 info 輸入值')
            測試命令列('echo ' + 'a' * 150 + '\n', 'a' * 123)
            串行值.sendall(b'halt\n')
            等待(lambda: 頭文件('HALTED'), '停機執行狀態 命令')
            assert b'PANIC' not in 日誌記錄 and b'SELFTEST FAIL' not in 日誌記錄
            print('PASS: {} 啓動, Java 內建 測試, 串行值 命令, PS/2 輸入值, 分配存儲裝置/發回結果, 停機執行狀態'.format(種類值))
            return 日誌記錄.decode('utf-8', 'replace')
        finally:
            串行值.close()
            監視器值.close()
            程序值.terminate()
            try:
                程序值.wait(timeout=3)
            except subprocess.TimeoutExpired:
                程序值.kill()
                程序值.wait()


if __name__ == '__main__':
    結果 = {種類值: 測試(種類值) for 種類值 in ('elf', 'iso')}
    (位置 / 'build/啓動測試.json').write_text(json.dumps(結果, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
