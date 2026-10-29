#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. ホスト 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from 命令実行 import 命令


def 起動処理():
    引数解析器 = argparse.ArgumentParser(description=__doc__)
    引数解析器.add_argument('file', type=Path)
    引数解析器.add_argument('arguments', nargs='*')
    引数解析器.add_argument('--class-name', help='패키지가 있는 .class의 전체 名前(예: 妥当性検査.束試験)')
    引数解析器.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 呼出 ABI 使用値')
    引数解析器.add_argument('--vnc', help='예: 127.0.0.1:2')
    引数解析器.add_argument('--include', action='append', type=Path, default=[], help='入口追記 class ファイル 또는 class 디렉터리(패키지 名前 値維持)')
    引数配列 = 引数解析器.parse_args()
    データ = 引数配列.file.read_bytes()
    if 引数配列.class_name and 引数配列.file.suffix != '.class': 引数解析器.error('--class-name은 .class 입력에서 사용합니다.')
    名前 = 引数配列.class_name + '.class' if 引数配列.class_name else 引数配列.file.name
    if len(データ) > 16384 or not 1 <= len(名前.encode('utf-8')) <= 63 or '\n' in 名前 or '\r' in 名前:
        引数解析器.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    分類値 = '.elf' if データ[:4] == b'\x7fELF' else 引数配列.file.suffix
    if 引数配列.linux and 分類値 != '.elf': 引数解析器.error('--linux는 ELF 바이너리에만 사용합니다.')
    if 分類値 not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        引数解析器.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(引数配列.arguments) > 7 or any(len(文字列データ.encode('utf-8')) > 255 or '\n' in 文字列データ or '\r' in 文字列データ for 文字列データ in 引数配列.arguments):
        引数解析器.error('인수는 最大値 7개, 각각 UTF-8 255바이트 이하입니다.')
    選択項目 = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if 引数配列.vnc: 選択項目 += ['-vnc', 引数配列.vnc]
    プロセス = subprocess.Popen(命令() + 選択項目, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    準備監視器 = selectors.DefaultSelector(); 準備監視器.register(プロセス.stdout, selectors.EVENT_READ)
    def メッセージ受取(標識, 実行状態待機期限=45):
        出力結果 = bytearray(); 終端位置変位量 = time.monotonic() + 実行状態待機期限
        while 標識 not in 出力結果:
            if time.monotonic() > 終端位置変位量: raise RuntimeError('UART timeout: ' + 出力結果.decode('utf-8', 'replace'))
            for 押下済み値, _ in 準備監視器.select(0.1):
                断片値 = 押下済み値.fileobj.read(4096)
                if 断片値: 出力結果.extend(断片値)
            if b'PANIC:' in 出力結果 or b'FAIL ' in 出力結果: raise RuntimeError(出力結果.decode('utf-8', 'replace'))
            if プロセス.poll() is not None: raise RuntimeError('QEMU exited: ' + 出力結果.decode('utf-8', 'replace'))
        return bytes(出力結果)
    def 送信(行, 標識=b'jkoros-native> '):
        プロセス.stdin.write(行.encode('utf-8') + b'\n'); プロセス.stdin.flush()
        return メッセージ受取(標識)
    def 命令実行(行):
        出力結果 = 送信(行); sys.stdout.buffer.write(出力結果); sys.stdout.buffer.flush()
        判定等価 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 出力結果)
        if not 判定等価: raise RuntimeError('guest did not report exit status')
        return int(判定等価.group(1))
    try:
        メッセージ受取(b'jkoros-native> ')
        ファイル一覧 = []
        for 包含項目 in 引数配列.include:
            if 包含項目.is_dir():
                ファイル一覧 += [(str(データ位置.relative_to(包含項目).with_suffix('')).replace('/', '.') + '.class', データ位置.read_bytes()) for データ位置 in sorted(包含項目.rglob('*.class'))]
            else:
                ファイル一覧.append((包含項目.name, 包含項目.read_bytes()))
        ファイル一覧 = [(項目個数, 宛先データ) for 項目個数, 宛先データ in ファイル一覧 if 項目個数 != 名前] + [(名前, データ)]
        for 送出転送名前, 送出転送データ in ファイル一覧:
            if len(送出転送データ) > 16384 or len(送出転送名前.encode('utf-8')) > 63 or '\n' in 送出転送名前 or '\r' in 送出転送名前:
                raise ValueError('入口追記 파일의 名前/容量 上限値 초과: ' + 送出転送名前)
            送信('load ' + shlex.quote(送出転送名前), b'hex> ')
            for 序数添字 in range(0, len(送出転送データ), 64): 送信(送出転送データ[序数添字:序数添字+64].hex(), b'hex> ')
            if b'LOADED' not in 送信('.'): raise RuntimeError('upload failed: ' + 送出転送名前)
            書出済み = 送信('hex ' + shlex.quote(送出転送名前))
            判定等価 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 書出済み, re.S)
            if not 判定等価 or bytes.fromhex(''.join(判定等価.group(2).decode().split())) != 送出転送データ: raise RuntimeError('upload verification failed')
        if 分類値 == '.java' and 命令実行('javac ' + shlex.quote(名前)) != 0: return 1
        実行形式イメージ = 引数配列.file.stem + '.elf'
        if 分類値 == '.c' and 命令実行('cc ' + shlex.quote(名前) + ' -o ' + shlex.quote(実行形式イメージ)) != 0: return 1
        実行項目 = 'java ' + shlex.quote(引数配列.class_name or 引数配列.file.stem) if 分類値 in ('.java', '.class') else ('python ' if 分類値 == '.py' else 'run ') + shlex.quote(名前)
        if 分類値 == '.jar': 実行項目 = 'java -jar ' + shlex.quote(名前)
        if 分類値 == '.c': 実行項目 = 'run ' + shlex.quote(実行形式イメージ)
        if 引数配列.linux: 実行項目 = 'run --linux ' + shlex.quote(名前)
        if 引数配列.arguments: 実行項目 += ' ' + ' '.join(shlex.quote(文字列データ) for 文字列データ in 引数配列.arguments)
        return 0 if 命令実行(実行項目) == 0 else 1
    finally:
        if プロセス.poll() is None:
            プロセス.terminate()
            try: プロセス.wait(timeout=5)
            except subprocess.TimeoutExpired: プロセス.kill(); プロセス.wait(timeout=5)
        準備監視器.close(); プロセス.stdin.close(); プロセス.stdout.close()


if __name__ == '__main__':
    raise SystemExit(起動処理())
