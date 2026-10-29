#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. konak 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from yürütmek_komut import komut


def çalıştır():
    ayrıştırıcı = argparse.ArgumentParser(description=__doc__)
    ayrıştırıcı.add_argument('file', type=Path)
    ayrıştırıcı.add_argument('arguments', nargs='*')
    ayrıştırıcı.add_argument('--class-name', help='패키지가 있는 .class의 전체 İsim(예: doğrulamak_5fb2b747.test_paket_iş)')
    ayrıştırıcı.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI kullanmak_değer')
    ayrıştırıcı.add_argument('--vnc', help='예: 127.0.0.1:2')
    ayrıştırıcı.add_argument('--include', action='append', type=Path, default=[], help='Ekleme_girdi class dosya 또는 class 디렉터리(패키지 İsim 유지)')
    bağımsız_değişken_DİZİ = ayrıştırıcı.parse_args()
    veri = bağımsız_değişken_DİZİ.file.read_bytes()
    if bağımsız_değişken_DİZİ.class_name and bağımsız_değişken_DİZİ.file.suffix != '.class': ayrıştırıcı.error('--class-name은 .class 입력에서 사용합니다.')
    İsim = bağımsız_değişken_DİZİ.class_name + '.class' if bağımsız_değişken_DİZİ.class_name else bağımsız_değişken_DİZİ.file.name
    if len(veri) > 16384 or not 1 <= len(İsim.encode('utf-8')) <= 63 or '\n' in İsim or '\r' in İsim:
        ayrıştırıcı.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    alan_değer = '.elf' if veri[:4] == b'\x7fELF' else bağımsız_değişken_DİZİ.file.suffix
    if bağımsız_değişken_DİZİ.linux and alan_değer != '.elf': ayrıştırıcı.error('--linux는 ELF 바이너리에만 사용합니다.')
    if alan_değer not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        ayrıştırıcı.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(bağımsız_değişken_DİZİ.arguments) > 7 or any(len(dize_veri.encode('utf-8')) > 255 or '\n' in dize_veri or '\r' in dize_veri for dize_veri in bağımsız_değişken_DİZİ.arguments):
        ayrıştırıcı.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Seçenekler = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if bağımsız_değişken_DİZİ.vnc: Seçenekler += ['-vnc', bağımsız_değişken_DİZİ.vnc]
    Süreç = subprocess.Popen(komut() + Seçenekler, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    seçici = selectors.DefaultSelector(); seçici.register(Süreç.stdout, selectors.EVENT_READ)
    def almak_belge(işaret, yürütme_ZAMANAŞIMI=45):
        çıktı = bytearray(); Bitiş_Ofset = time.monotonic() + yürütme_ZAMANAŞIMI
        while işaret not in çıktı:
            if time.monotonic() > Bitiş_Ofset: raise RuntimeError('UART timeout: ' + çıktı.decode('utf-8', 'replace'))
            for 누름값, _ in seçici.select(0.1):
                parça_değer = 누름값.fileobj.read(4096)
                if parça_değer: çıktı.extend(parça_değer)
            if b'PANIC:' in çıktı or b'FAIL ' in çıktı: raise RuntimeError(çıktı.decode('utf-8', 'replace'))
            if Süreç.poll() is not None: raise RuntimeError('QEMU exited: ' + çıktı.decode('utf-8', 'replace'))
        return bytes(çıktı)
    def göndermek(girdi_satırı, işaret=b'jkoros-native> '):
        Süreç.stdin.write(girdi_satırı.encode('utf-8') + b'\n'); Süreç.stdin.flush()
        return almak_belge(işaret)
    def yürütmek_komut(girdi_satırı):
        çıktı = göndermek(girdi_satırı); sys.stdout.buffer.write(çıktı); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', çıktı)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        almak_belge(b'jkoros-native> ')
        dosya_listesi = []
        for içermek in bağımsız_değişken_DİZİ.include:
            if içermek.is_dir():
                dosya_listesi += [(str(veri_konum.relative_to(içermek).with_suffix('')).replace('/', '.') + '.class', veri_konum.read_bytes()) for veri_konum in sorted(içermek.rglob('*.class'))]
            else:
                dosya_listesi.append((içermek.name, içermek.read_bytes()))
        dosya_listesi = [(öğe_BAĞ_DEĞ_SAY, hedef_veri) for öğe_BAĞ_DEĞ_SAY, hedef_veri in dosya_listesi if öğe_BAĞ_DEĞ_SAY != İsim] + [(İsim, veri)]
        for yükle_ad, yükle_veri in dosya_listesi:
            if len(yükle_veri) > 16384 or len(yükle_ad.encode('utf-8')) > 63 or '\n' in yükle_ad or '\r' in yükle_ad:
                raise ValueError('Ekleme_girdi 파일의 İsim/Boyut 제한 초과: ' + yükle_ad)
            göndermek('load ' + shlex.quote(yükle_ad), b'hex> ')
            for 순번 in range(0, len(yükle_veri), 64): göndermek(yükle_veri[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in göndermek('.'): raise RuntimeError('upload failed: ' + yükle_ad)
            갈무리자료 = göndermek('hex ' + shlex.quote(yükle_ad))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != yükle_veri: raise RuntimeError('upload verification failed')
        if alan_değer == '.java' and yürütmek_komut('javac ' + shlex.quote(İsim)) != 0: return 1
        yürütülebilir_RESİM = bağımsız_değişken_DİZİ.file.stem + '.elf'
        if alan_değer == '.c' and yürütmek_komut('cc ' + shlex.quote(İsim) + ' -o ' + shlex.quote(yürütülebilir_RESİM)) != 0: return 1
        program = 'java ' + shlex.quote(bağımsız_değişken_DİZİ.class_name or bağımsız_değişken_DİZİ.file.stem) if alan_değer in ('.java', '.class') else ('python ' if alan_değer == '.py' else 'run ') + shlex.quote(İsim)
        if alan_değer == '.jar': program = 'java -jar ' + shlex.quote(İsim)
        if alan_değer == '.c': program = 'run ' + shlex.quote(yürütülebilir_RESİM)
        if bağımsız_değişken_DİZİ.linux: program = 'run --linux ' + shlex.quote(İsim)
        if bağımsız_değişken_DİZİ.arguments: program += ' ' + ' '.join(shlex.quote(dize_veri) for dize_veri in bağımsız_değişken_DİZİ.arguments)
        return 0 if yürütmek_komut(program) == 0 else 1
    finally:
        if Süreç.poll() is None:
            Süreç.terminate()
            try: Süreç.wait(timeout=5)
            except subprocess.TimeoutExpired: Süreç.kill(); Süreç.wait(timeout=5)
        seçici.close(); Süreç.stdin.close(); Süreç.stdout.close()


if __name__ == '__main__':
    raise SystemExit(çalıştır())
