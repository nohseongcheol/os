#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import àfojúunúṣe_maṣíìnì

위치 = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', 위치 / 'Àwọn_irinṣẹ́/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def ṣàtúnṣe_iye(maṣíìnì, Àkóónú_iye):
    Rọ́ọ̀nù = len(maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú)
    maṣíìnì.직렬.sendall(('edit note.txt\n' + Àkóónú_iye + '\n.save\n').encode())
    return maṣíìnì.기다림('jkoros> ', Rọ́ọ̀nù)

def ṣiṣẹ́_àṣẹ():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.Ṣẹ̀dá_ìgbéwọlé(매체)
        maṣíìnì = àfojúunúṣe_maṣíìnì(위치 / 'build/kernel.elf', 저장매체=매체)
        try:
            maṣíìnì.Àṣẹ('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            ṣàtúnṣe_iye(maṣíìnì, 'generation-one')
            maṣíìnì.Àṣẹ('sync', ['Sync: 0'])
            ṣàtúnṣe_iye(maṣíìnì, 'generation-two')
            maṣíìnì.Àṣẹ('sync', ['Sync: 0'])
            ṣàtúnṣe_iye(maṣíìnì, 'unsynced-three')
            결과['save'] = maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú.decode('utf-8', 'replace')
        finally:
            maṣíìnì.Ti()
        maṣíìnì = àfojúunúṣe_maṣíìnì(위치 / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            출력 = maṣíìnì.Àṣẹ('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            maṣíìnì.Àṣẹ('cat stored.txt', ['saved-from-C'])
            결과['restore'] = maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú.decode('utf-8', 'replace')
        finally:
            maṣíìnì.Ti()
        détà = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', détà, (1 + wá_atọ̀ka_àkóónú * 259) * 512 + 4)[0] for wá_atọ̀ka_àkóónú in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        détà[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(détà)
        maṣíìnì = àfojúunúṣe_maṣíìnì(위치 / 'build/kernel.elf', 저장매체=매체)
        try:
            maṣíìnì.Àṣẹ('cat note.txt', ['generation-one'])
            maṣíìnì.Àṣẹ('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú.decode('utf-8', 'replace')
        finally:
            maṣíìnì.Ti()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        maṣíìnì = àfojúunúṣe_maṣíìnì(위치 / 'build/kernel.elf', 저장매체=다른매체)
        try:
            maṣíìnì.Àṣẹ('sync', ['Sync: -19'])
        finally:
            maṣíìnì.Ti()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (위치 / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_iye/ISO 재부팅/검사합 ràpadà_ipò/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    ṣiṣẹ́_àṣẹ()
