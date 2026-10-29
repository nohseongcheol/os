#!/usr/bin/env python3
"""konak libc 없이 연결한 Türkçe C 프로그램을 fiili_veri ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from test_kullanıcı_ağ import VM

konum = Path(__file__).resolve().parents[1]

def yürütmek_komut():
    sonuç = {}
    sunucu_değer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sunucu_değer.bind(('127.0.0.1', 0))
    sunucu_değer.settimeout(0.1)
    bağlantı_noktası_numarası = sunucu_değer.getsockname()[1]
    GETİRİ_veri = []
    끝냄 = threading.Event()
    def yankı_yanıt():
        while not 끝냄.is_set():
            try:
                veri, ADRES = sunucu_değer.recvfrom(4096)
            except socket.timeout:
                continue
            GETİRİ_veri.append(veri)
            sunucu_değer.sendto(veri, ADRES)
    çalışan_değer = threading.Thread(target=yankı_yanıt, daemon=True)
    çalışan_değer.start()
    try:
        for Tip_değer in ('elf', 'iso'):
            makine = VM(konum / ('build/kernel.' + Tip_değer), Tip_değer)
            try:
                for öğe_değer_58902391 in range(2):
                    makine.komut('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    makine.komut('run posixudp ' + str(bağlantı_noktası_numarası), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                çalıştır = len(makine.LOG_KAYIT)
                makine.직렬.sendall(b'run posixinput\n')
                makine.bekleme_durumu('POSIX INPUT READY', çalıştır)
                makine.직렬.sendall(b'abcdef')
                metinÇıktısı = makine.bekleme_durumu('jkoros> ', çalıştır)
                assert 'POSIX INPUT PASS' in metinÇıktısı and 'Exit: 0' in metinÇıktısı, metinÇıktısı
                makine.komut('javac Hello.java', ['Exit: 0'])
                makine.komut('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                makine.komut('run hello recovered', ['arg: recovered', 'Exit: 0'])
                sonuç[Tip_değer] = makine.LOG_KAYIT.decode('utf-8', 'replace')
                print('PASS:', Tip_değer, 'POSIX dosya/공유 konum/삭제 수명/ADRES korumak_değer/UDP/표준 artış_değer/기존 Java', flush=True)
            finally:
                makine.Kapat()
        assert b'posix-udp' in GETİRİ_veri and b'truncate' in GETİRİ_veri and b'' in GETİRİ_veri
    finally:
        끝냄.set(); çalışan_değer.join(timeout=2); sunucu_değer.close()
    sonuç['host_datagrams'] = [veri.decode() for veri in GETİRİ_veri]
    (konum / 'build/iş_test.json').write_text(json.dumps(sonuç, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    yürütmek_komut()
