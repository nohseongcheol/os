#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. Chủ 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from thựcThiLệnh import lệnh


def chạy():
    bộPhânTích = argparse.ArgumentParser(description=__doc__)
    bộPhânTích.add_argument('file', type=Path)
    bộPhânTích.add_argument('arguments', nargs='*')
    bộPhânTích.add_argument('--class-name', help='패키지가 있는 .class의 전체 tên(예: thẩmĐịnh.thửGóiGộp)')
    bộPhânTích.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 gọiThựcHiện ABI giáTrịDùng')
    bộPhânTích.add_argument('--vnc', help='예: 127.0.0.1:2')
    bộPhânTích.add_argument('--include', action='append', type=Path, default=[], help='thêmCuốiMục class Tệp 또는 class 디렉터리(패키지 tên giữLạiGiáTrị)')
    mảngĐốiSố = bộPhânTích.parse_args()
    DữLiệu = mảngĐốiSố.file.read_bytes()
    if mảngĐốiSố.class_name and mảngĐốiSố.file.suffix != '.class': bộPhânTích.error('--class-name은 .class 입력에서 사용합니다.')
    tên = mảngĐốiSố.class_name + '.class' if mảngĐốiSố.class_name else mảngĐốiSố.file.name
    if len(DữLiệu) > 16384 or not 1 <= len(tên.encode('utf-8')) <= 63 or '\n' in tên or '\r' in tên:
        bộPhânTích.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    giáTrịLoạiMục = '.elf' if DữLiệu[:4] == b'\x7fELF' else mảngĐốiSố.file.suffix
    if mảngĐốiSố.linux and giáTrịLoạiMục != '.elf': bộPhânTích.error('--linux는 ELF 바이너리에만 사용합니다.')
    if giáTrịLoạiMục not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        bộPhânTích.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(mảngĐốiSố.arguments) > 7 or any(len(dữLiệuChuỗi.encode('utf-8')) > 255 or '\n' in dữLiệuChuỗi or '\r' in dữLiệuChuỗi for dữLiệuChuỗi in mảngĐốiSố.arguments):
        bộPhânTích.error('인수는 giáTrịTốiĐa 7개, 각각 UTF-8 255바이트 이하입니다.')
    cácTùyChọn = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if mảngĐốiSố.vnc: cácTùyChọn += ['-vnc', mảngĐốiSố.vnc]
    tiếnTrình = subprocess.Popen(lệnh() + cácTùyChọn, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    bộChọn = selectors.DefaultSelector(); bộChọn.register(tiếnTrình.stdout, selectors.EVENT_READ)
    def nhậnThôngĐiệp(dấuMốc, hếtGiờViệcThựcThi=45):
        đầuRa = bytearray(); độLệchKếtThúc = time.monotonic() + hếtGiờViệcThựcThi
        while dấuMốc not in đầuRa:
            if time.monotonic() > độLệchKếtThúc: raise RuntimeError('UART timeout: ' + đầuRa.decode('utf-8', 'replace'))
            for giáTrịĐãNhấn, _ in bộChọn.select(0.1):
                giáTrịĐoạn = giáTrịĐãNhấn.fileobj.read(4096)
                if giáTrịĐoạn: đầuRa.extend(giáTrịĐoạn)
            if b'PANIC:' in đầuRa or b'FAIL ' in đầuRa: raise RuntimeError(đầuRa.decode('utf-8', 'replace'))
            if tiếnTrình.poll() is not None: raise RuntimeError('QEMU exited: ' + đầuRa.decode('utf-8', 'replace'))
        return bytes(đầuRa)
    def gửi(dòng, dấuMốc=b'jkoros-native> '):
        tiếnTrình.stdin.write(dòng.encode('utf-8') + b'\n'); tiếnTrình.stdin.flush()
        return nhậnThôngĐiệp(dấuMốc)
    def thựcThiLệnh(dòng):
        đầuRa = gửi(dòng); sys.stdout.buffer.write(đầuRa); sys.stdout.buffer.flush()
        làBằng = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', đầuRa)
        if not làBằng: raise RuntimeError('guest did not report exit status')
        return int(làBằng.group(1))
    try:
        nhậnThôngĐiệp(b'jkoros-native> ')
        danhSáchTệp = []
        for baoGồm in mảngĐốiSố.include:
            if baoGồm.is_dir():
                danhSáchTệp += [(str(vịTríDữLiệu.relative_to(baoGồm).with_suffix('')).replace('/', '.') + '.class', vịTríDữLiệu.read_bytes()) for vịTríDữLiệu in sorted(baoGồm.rglob('*.class'))]
            else:
                danhSáchTệp.append((baoGồm.name, baoGồm.read_bytes()))
        danhSáchTệp = [(sốLượngPhầnMục, dữLiệuĐích) for sốLượngPhầnMục, dữLiệuĐích in danhSáchTệp if sốLượngPhầnMục != tên] + [(tên, DữLiệu)]
        for tênTảiLên, dữLiệuTảiLên in danhSáchTệp:
            if len(dữLiệuTảiLên) > 16384 or len(tênTảiLên.encode('utf-8')) > 63 or '\n' in tênTảiLên or '\r' in tênTảiLên:
                raise ValueError('thêmCuốiMục 파일의 tên/cỡ giáTrịGiớiHạn 초과: ' + tênTảiLên)
            gửi('load ' + shlex.quote(tênTảiLên), b'hex> ')
            for chỉSốThứBậc in range(0, len(dữLiệuTảiLên), 64): gửi(dữLiệuTảiLên[chỉSốThứBậc:chỉSốThứBậc+64].hex(), b'hex> ')
            if b'LOADED' not in gửi('.'): raise RuntimeError('upload failed: ' + tênTảiLên)
            đãKếtXuất = gửi('hex ' + shlex.quote(tênTảiLên))
            làBằng = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', đãKếtXuất, re.S)
            if not làBằng or bytes.fromhex(''.join(làBằng.group(2).decode().split())) != dữLiệuTảiLên: raise RuntimeError('upload verification failed')
        if giáTrịLoạiMục == '.java' and thựcThiLệnh('javac ' + shlex.quote(tên)) != 0: return 1
        ảnhTệpThựcThi = mảngĐốiSố.file.stem + '.elf'
        if giáTrịLoạiMục == '.c' and thựcThiLệnh('cc ' + shlex.quote(tên) + ' -o ' + shlex.quote(ảnhTệpThựcThi)) != 0: return 1
        chươngTrình = 'java ' + shlex.quote(mảngĐốiSố.class_name or mảngĐốiSố.file.stem) if giáTrịLoạiMục in ('.java', '.class') else ('python ' if giáTrịLoạiMục == '.py' else 'run ') + shlex.quote(tên)
        if giáTrịLoạiMục == '.jar': chươngTrình = 'java -jar ' + shlex.quote(tên)
        if giáTrịLoạiMục == '.c': chươngTrình = 'run ' + shlex.quote(ảnhTệpThựcThi)
        if mảngĐốiSố.linux: chươngTrình = 'run --linux ' + shlex.quote(tên)
        if mảngĐốiSố.arguments: chươngTrình += ' ' + ' '.join(shlex.quote(dữLiệuChuỗi) for dữLiệuChuỗi in mảngĐốiSố.arguments)
        return 0 if thựcThiLệnh(chươngTrình) == 0 else 1
    finally:
        if tiếnTrình.poll() is None:
            tiếnTrình.terminate()
            try: tiếnTrình.wait(timeout=5)
            except subprocess.TimeoutExpired: tiếnTrình.kill(); tiếnTrình.wait(timeout=5)
        bộChọn.close(); tiếnTrình.stdin.close(); tiếnTrình.stdout.close()


if __name__ == '__main__':
    raise SystemExit(chạy())
