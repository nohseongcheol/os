#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 直列値/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

位置 = Path(__file__).resolve().parents[1]


def 待機(検査項目, 説明, 上限値=15):
    終端 = time.monotonic() + 上限値
    while time.monotonic() < 終端:
        結果 = 検査項目()
        if 結果:
            return 結果
        time.sleep(0.05)
    raise AssertionError('時間値 초과: ' + 説明)


def 試験(種別値):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 一時値:
        一時値 = Path(一時値)
        直列経路 = 一時値 / 'serial.sock'
        監視器経路 = 一時値 / 'monitor.sock'
        命令 = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(直列経路) + ',server,nowait',
                '-monitor', 'unix:' + str(監視器経路) + ',server,nowait']
        命令 += ['-kernel', str(位置 / 'build/kernel.elf')] if 種別値 == 'elf' else [
            '-cdrom', str(位置 / 'build/kernel.iso'), '-boot', 'd']
        # 直列値 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        命令 += ['-S']
        プロセス値 = subprocess.Popen(命令, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        直列値 = socket.socket(socket.AF_UNIX)
        監視器値 = socket.socket(socket.AF_UNIX)
        履歴記録記録 = bytearray()
        try:
            def ソケット用意():
                if プロセス値.poll() is not None:
                    raise AssertionError(プロセス値.stderr.read().decode('utf-8', 'replace'))
                return 直列経路.exists() and 監視器経路.exists()
            待機(ソケット用意, 'QEMU ソケット値')
            直列値.connect(str(直列経路))
            監視器値.connect(str(監視器経路))
            直列値.setblocking(False)
            監視器値.sendall(b'cont\n')

            def ヘッダー(文字列, 起動処理=0):
                読取, _, _ = select.select([直列値], [], [], 0.1)
                if 読取:
                    データ = 直列値.recv(65536)
                    if not データ:
                        raise AssertionError('直列値 接続 終了点プログラム')
                    履歴記録記録.extend(データ)
                if プロセス値.poll() is not None:
                    raise AssertionError('QEMU 비정상 終了点プログラム: ' + str(プロセス値.returncode))
                return 文字列.encode('utf-8') in 履歴記録記録[起動処理:]

            def 命令一覧試験(入力値, 期待状態):
                起動処理 = len(履歴記録記録)
                直列値.sendall(入力値.encode('ascii'))
                待機(lambda: ヘッダー(期待状態, 起動処理), 期待状態)
                待機(lambda: ヘッダー('jkoros> ', 起動処理), '命令 後続側状況 프롬프트')

            待機(lambda: ヘッダー('READY'), 種別値 + ' 起動')
            assert b'JAVA SELFTEST PASS' in 履歴記録記録
            assert 'Java 기계어 中核値 起動処理'.encode() in 履歴記録記録
            命令一覧試験('info\r\n', 'embedded subset JVM / polling kernel')
            命令一覧試験('help\n', 'free N | echo TEXT')
            命令一覧試験('mem\n', ' / 8 (각 4096바이트)')
            命令一覧試験('echo natix\bve\n', 'native\r\n')
            for 番号 in range(8):
                命令一覧試験('alloc\n', '区画値 番号: ' + str(番号))
            命令一覧試験('alloc\n', '区画値 番号: -1')
            命令一覧試験('free 3\n', '반환됨')
            命令一覧試験('free 3\n', '할당되지 않은 区画値')
            命令一覧試験('free 99\n', '사용법: free 0..7')
            命令一覧試験('alloc\n', '区画値 番号: 3')
            命令一覧試験('free 0\n', '반환됨')
            命令一覧試験('test\n', 'JAVA SELFTEST PASS')
            命令一覧試験('unknown\n', '알 数 없는 명령입니다')
            命令一覧試験('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            起動処理 = len(履歴記録記録)
            for キー値 in ('i', 'n', 'f', 'o', 'ret'):
                監視器値.sendall(('sendkey ' + キー値 + ' 30\n').encode())
                time.sleep(0.09)
            待機(lambda: ヘッダー('embedded subset JVM / polling kernel', 起動処理), 'PS/2 info 入力値')
            命令一覧試験('echo ' + 'a' * 150 + '\n', 'a' * 123)
            直列値.sendall(b'halt\n')
            待機(lambda: ヘッダー('HALTED'), '機械停止実行状態 命令')
            assert b'PANIC' not in 履歴記録記録 and b'SELFTEST FAIL' not in 履歴記録記録
            print('PASS: {} 起動, Java 内蔵 試験, 直列値 命令, PS/2 入力値, 記憶装置確保/復帰結果, 機械停止実行状態'.format(種別値))
            return 履歴記録記録.decode('utf-8', 'replace')
        finally:
            直列値.close()
            監視器値.close()
            プロセス値.terminate()
            try:
                プロセス値.wait(timeout=3)
            except subprocess.TimeoutExpired:
                プロセス値.kill()
                プロセス値.wait()


if __name__ == '__main__':
    結果 = {種別値: 試験(種別値) for 種別値 in ('elf', 'iso')}
    (位置 / 'build/起動試験.json').write_text(json.dumps(結果, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
