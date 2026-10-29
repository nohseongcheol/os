#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import ຈໍາລອງ_ເຄື່ອງຈັກ

ຈັດຕໍາແຫນ່ງ = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('ມີເດຍ_ເຄື່ອງມື', ຈັດຕໍາແຫນ່ງ / 'ເຄື່ອງມື/ສ້າງ_ບ່ອນເກັບຂໍ້ມູນ_ມີເດຍ.py')
ມີເດຍ_ເຄື່ອງມື = importlib.util.module_from_spec(명세)
명세.loader.exec_module(ມີເດຍ_ເຄື່ອງມື)

def ແກ້ໄຂ_ຄ່າ(ເຄື່ອງຈັກ, ເນື້ອໃນ_ຄ່າ_cb0f2404):
    ແລ່ນ = len(ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ)
    ເຄື່ອງຈັກ.직렬.sendall(('edit note.txt\n' + ເນື້ອໃນ_ຄ່າ_cb0f2404 + '\n.save\n').encode())
    return ເຄື່ອງຈັກ.ລໍຖ້າ_ສະຖານະ('jkoros> ', ແລ່ນ)

def ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ():
    ມາດຕະການ = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        ມີເດຍ_ຄ່າ = Path(임시) / 'files.img'
        ມີເດຍ_ເຄື່ອງມື.ສ້າງ_ເຂົ້າໃນ(ມີເດຍ_ຄ່າ)
        ເຄື່ອງຈັກ = ຈໍາລອງ_ເຄື່ອງຈັກ(ຈັດຕໍາແຫນ່ງ / 'build/kernel.elf', 저장매체=ມີເດຍ_ຄ່າ)
        try:
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            ແກ້ໄຂ_ຄ່າ(ເຄື່ອງຈັກ, 'generation-one')
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('sync', ['Sync: 0'])
            ແກ້ໄຂ_ຄ່າ(ເຄື່ອງຈັກ, 'generation-two')
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('sync', ['Sync: 0'])
            ແກ້ໄຂ_ຄ່າ(ເຄື່ອງຈັກ, 'unsynced-three')
            ມາດຕະການ['save'] = ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ.decode('utf-8', 'replace')
        finally:
            ເຄື່ອງຈັກ.ປິດ()
        ເຄື່ອງຈັກ = ຈໍາລອງ_ເຄື່ອງຈັກ(ຈັດຕໍາແຫນ່ງ / 'build/kernel.iso', 'iso', 저장매체=ມີເດຍ_ຄ່າ)
        try:
            출력 = ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('cat stored.txt', ['saved-from-C'])
            ມາດຕະການ['restore'] = ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ.decode('utf-8', 'replace')
        finally:
            ເຄື່ອງຈັກ.ປິດ()
        ຂໍ້ມູນ = bytearray(ມີເດຍ_ຄ່າ.read_bytes())
        세대들 = [struct.unpack_from('<I', ຂໍ້ມູນ, (1 + ດັດຊະນີ * 259) * 512 + 4)[0] for ດັດຊະນີ in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        ຂໍ້ມູນ[(1 + 최신 * 259 + 3) * 512] ^= 1
        ມີເດຍ_ຄ່າ.write_bytes(ຂໍ້ມູນ)
        ເຄື່ອງຈັກ = ຈໍາລອງ_ເຄື່ອງຈັກ(ຈັດຕໍາແຫນ່ງ / 'build/kernel.elf', 저장매체=ມີເດຍ_ຄ່າ)
        try:
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('cat note.txt', ['generation-one'])
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('cat stored.txt', ['saved-from-C'])
            ມາດຕະການ['checksum_fallback'] = ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ.decode('utf-8', 'replace')
        finally:
            ເຄື່ອງຈັກ.ປິດ()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        ເຄື່ອງຈັກ = ຈໍາລອງ_ເຄື່ອງຈັກ(ຈັດຕໍາແຫນ່ງ / 'build/kernel.elf', 저장매체=다른매체)
        try:
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('sync', ['Sync: -19'])
        finally:
            ເຄື່ອງຈັກ.ປິດ()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        ມາດຕະການ['foreign_disk_unchanged'] = True
    (ຈັດຕໍາແຫນ່ງ / 'build/보존시험.json').write_text(json.dumps(ມາດຕະການ, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE ຮ້ານຄ້າ_ຄ່າ/ISO 재부팅/검사합 복구/다른 ມີເດຍ_ຄ່າ 비변경', flush=True)

if __name__ == '__main__':
    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()
