#!/usr/bin/env python3
"""ホスト libc 없이 연결한 日本語 C 프로그램을 実際データ ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 利用者通信網試験 import 仮想機械

位置 = Path(__file__).resolve().parents[1]

def 命令実行():
    結果 = {}
    サーバー値 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    サーバー値.bind(('127.0.0.1', 0))
    サーバー値.settimeout(0.1)
    ポート番号 = サーバー値.getsockname()[1]
    受信済みデータ = []
    終了状態状況 = threading.Event()
    def 復唱返答():
        while not 終了状態状況.is_set():
            try:
                データ, 番地 = サーバー値.recvfrom(4096)
            except socket.timeout:
                continue
            受信済みデータ.append(データ)
            サーバー値.sendto(データ, 番地)
    作業担当値 = threading.Thread(target=復唱返答, daemon=True)
    作業担当値.start()
    try:
        for 種別値 in ('elf', 'iso'):
            機械 = 仮想機械(位置 / ('build/kernel.' + 種別値), 種別値)
            try:
                for 反復回値 in range(2):
                    機械.命令('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    機械.命令('run posixudp ' + str(ポート番号), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                起動処理 = len(機械.履歴記録記録)
                機械.直列値.sendall(b'run posixinput\n')
                機械.状況待合('POSIX INPUT READY', 起動処理)
                機械.直列値.sendall(b'abcdef')
                出力 = 機械.状況待合('jkoros> ', 起動処理)
                assert 'POSIX INPUT PASS' in 出力 and 'Exit: 0' in 出力, 出力
                機械.命令('javac Hello.java', ['Exit: 0'])
                機械.命令('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                機械.命令('run hello recovered', ['arg: recovered', 'Exit: 0'])
                結果[種別値] = 機械.履歴記録記録.decode('utf-8', 'replace')
                print('PASS:', 種別値, 'POSIX ファイル/공유 位置/삭제 수명/番地 値防護/UDP/표준 入力値/기존 Java', flush=True)
            finally:
                機械.閉鎖()
        assert b'posix-udp' in 受信済みデータ and b'truncate' in 受信済みデータ and b'' in 受信済みデータ
    finally:
        終了状態状況.set(); 作業担当値.join(timeout=2); サーバー値.close()
    結果['host_datagrams'] = [データ.decode() for データ in 受信済みデータ]
    (位置 / 'build/契約試験.json').write_text(json.dumps(結果, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    命令実行()
