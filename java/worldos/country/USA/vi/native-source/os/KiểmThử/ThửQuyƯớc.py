#!/usr/bin/env python3
"""Chủ libc 없이 연결한 tiếngViệt C 프로그램을 dữLiệuThựcTế ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from thửMạngNgườiDùng import MáyẢo

vịTrí = Path(__file__).resolve().parents[1]

def thựcThiLệnh():
    kếtQuả = {}
    giáTrịMáyChủ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    giáTrịMáyChủ.bind(('127.0.0.1', 0))
    giáTrịMáyChủ.settimeout(0.1)
    sốCổng = giáTrịMáyChủ.getsockname()[1]
    dữLiệuĐãNhận = []
    trạngTháiViệcChấmDứt = threading.Event()
    def lờiĐápVọngLại():
        while not trạngTháiViệcChấmDứt.is_set():
            try:
                DữLiệu, địaChỉ = giáTrịMáyChủ.recvfrom(4096)
            except socket.timeout:
                continue
            dữLiệuĐãNhận.append(DữLiệu)
            giáTrịMáyChủ.sendto(DữLiệu, địaChỉ)
    giáTrịBộLàmViệc = threading.Thread(target=lờiĐápVọngLại, daemon=True)
    giáTrịBộLàmViệc.start()
    try:
        for giáTrịLoại in ('elf', 'iso'):
            máy = MáyẢo(vịTrí / ('build/kernel.' + giáTrịLoại), giáTrịLoại)
            try:
                for giáTrịLầnLặp in range(2):
                    máy.lệnh('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    máy.lệnh('run posixudp ' + str(sốCổng), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                chạy = len(máy.bảnGhiNhậtKý)
                máy.giáTrịNốiTiếp.sendall(b'run posixinput\n')
                máy.chờTrạngThái('POSIX INPUT READY', chạy)
                máy.giáTrịNốiTiếp.sendall(b'abcdef')
                ĐầuRa = máy.chờTrạngThái('jkoros> ', chạy)
                assert 'POSIX INPUT PASS' in ĐầuRa and 'Exit: 0' in ĐầuRa, ĐầuRa
                máy.lệnh('javac Hello.java', ['Exit: 0'])
                máy.lệnh('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                máy.lệnh('run hello recovered', ['arg: recovered', 'Exit: 0'])
                kếtQuả[giáTrịLoại] = máy.bảnGhiNhậtKý.decode('utf-8', 'replace')
                print('PASS:', giáTrịLoại, 'POSIX Tệp/공유 vịTrí/삭제 수명/địaChỉ bảoVệGiáTrị/UDP/표준 giáTrịVào/기존 Java', flush=True)
            finally:
                máy.đóng()
        assert b'posix-udp' in dữLiệuĐãNhận and b'truncate' in dữLiệuĐãNhận and b'' in dữLiệuĐãNhận
    finally:
        trạngTháiViệcChấmDứt.set(); giáTrịBộLàmViệc.join(timeout=2); giáTrịMáyChủ.close()
    kếtQuả['host_datagrams'] = [DữLiệu.decode() for DữLiệu in dữLiệuĐãNhận]
    (vịTrí / 'build/ThửQuyƯớc.json').write_text(json.dumps(kếtQuả, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    thựcThiLệnh()
