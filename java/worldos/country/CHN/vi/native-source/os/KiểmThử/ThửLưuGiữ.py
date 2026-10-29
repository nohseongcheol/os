#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 saoChépĐãGiữNguyên 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from thửMạngNgườiDùng import MáyẢo

vịTrí = Path(__file__).resolve().parents[1]
đặcTả = importlib.util.spec_from_file_location('côngCụPhươngTiện', vịTrí / 'CôngCụ/TạoPhươngTiệnLưu.py')
côngCụPhươngTiện = importlib.util.module_from_spec(đặcTả)
đặcTả.loader.exec_module(côngCụPhươngTiện)

def giáTrịSửa(máy, giáTrịNộiDung):
    chạy = len(máy.bảnGhiNhậtKý)
    máy.giáTrịNốiTiếp.sendall(('edit note.txt\n' + giáTrịNộiDung + '\n.save\n').encode())
    return máy.chờTrạngThái('jkoros> ', chạy)

def thựcThiLệnh():
    kếtQuả = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as giáTrịTạm:
        giáTrịPhươngTiện = Path(giáTrịTạm) / 'files.img'
        côngCụPhươngTiện.tạoMục(giáTrịPhươngTiện)
        máy = MáyẢo(vịTrí / 'build/kernel.elf', môiGiớiLưuTrữ=giáTrịPhươngTiện)
        try:
            máy.lệnh('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            giáTrịSửa(máy, 'generation-one')
            máy.lệnh('sync', ['Sync: 0'])
            giáTrịSửa(máy, 'generation-two')
            máy.lệnh('sync', ['Sync: 0'])
            giáTrịSửa(máy, 'unsynced-three')
            kếtQuả['save'] = máy.bảnGhiNhậtKý.decode('utf-8', 'replace')
        finally:
            máy.đóng()
        máy = MáyẢo(vịTrí / 'build/kernel.iso', 'iso', môiGiớiLưuTrữ=giáTrịPhươngTiện)
        try:
            ĐầuRa = máy.lệnh('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in ĐầuRa
            máy.lệnh('cat stored.txt', ['saved-from-C'])
            kếtQuả['restore'] = máy.bảnGhiNhậtKý.decode('utf-8', 'replace')
        finally:
            máy.đóng()
        DữLiệu = bytearray(giáTrịPhươngTiện.read_bytes())
        danhSáchCácThếHệ = [struct.unpack_from('<I', DữLiệu, (1 + sốHiệu * 259) * 512 + 4)[0] for sốHiệu in (0, 1)]
        giáTrịMớiNhất = 0 if danhSáchCácThếHệ[0] > danhSáchCácThếHệ[1] else 1
        DữLiệu[(1 + giáTrịMớiNhất * 259 + 3) * 512] ^= 1
        giáTrịPhươngTiện.write_bytes(DữLiệu)
        máy = MáyẢo(vịTrí / 'build/kernel.elf', môiGiớiLưuTrữ=giáTrịPhươngTiện)
        try:
            máy.lệnh('cat note.txt', ['generation-one'])
            máy.lệnh('cat stored.txt', ['saved-from-C'])
            kếtQuả['checksum_fallback'] = máy.bảnGhiNhậtKý.decode('utf-8', 'replace')
        finally:
            máy.đóng()
        phươngTiệnKhác = Path(giáTrịTạm) / 'foreign.img'
        phươngTiệnKhác.write_bytes(bytes([0x5a]) * (2048 * 512))
        phầnMụcTrướcĐó = hashlib.sha256(phươngTiệnKhác.read_bytes()).hexdigest()
        máy = MáyẢo(vịTrí / 'build/kernel.elf', môiGiớiLưuTrữ=phươngTiệnKhác)
        try:
            máy.lệnh('sync', ['Sync: -19'])
        finally:
            máy.đóng()
        assert hashlib.sha256(phươngTiệnKhác.read_bytes()).hexdigest() == phầnMụcTrướcĐó
        kếtQuả['foreign_disk_unchanged'] = True
    (vịTrí / 'build/ThửLưuGiữ.json').write_text(json.dumps(kếtQuả, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE giáTrịCất/ISO 재부팅/tổngKiểm khôiPhụcTrạngThái/다른 giáTrịPhươngTiện 비변경', flush=True)

if __name__ == '__main__':
    thựcThiLệnh()
