#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import వర్చువల్_యంత్రం

స్థానము = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', స్థానము / 'ఉపకరణాలు/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def సంకలనంచేయు_మూల్యం(యంత్రం, విషయం_మూల్యం):
    నడుపుము = len(యంత్రం.లాగ్_వరుస)
    యంత్రం.직렬.sendall(('edit note.txt\n' + విషయం_మూల్యం + '\n.save\n').encode())
    return యంత్రం.వేచియుండు_స్థితి('jkoros> ', నడుపుము)

def అమలు_చేయి_ఆదేశం():
    ప్రమాణం = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.క్రియేట్_ప్రవేశం(매체)
        యంత్రం = వర్చువల్_యంత్రం(స్థానము / 'build/kernel.elf', 저장매체=매체)
        try:
            యంత్రం.ఆదేశము('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            సంకలనంచేయు_మూల్యం(యంత్రం, 'generation-one')
            యంత్రం.ఆదేశము('sync', ['Sync: 0'])
            సంకలనంచేయు_మూల్యం(యంత్రం, 'generation-two')
            యంత్రం.ఆదేశము('sync', ['Sync: 0'])
            సంకలనంచేయు_మూల్యం(యంత్రం, 'unsynced-three')
            ప్రమాణం['save'] = యంత్రం.లాగ్_వరుస.decode('utf-8', 'replace')
        finally:
            యంత్రం.మూసివేయి()
        యంత్రం = వర్చువల్_యంత్రం(స్థానము / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            అవుట్పుట్ = యంత్రం.ఆదేశము('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in అవుట్పుట్
            యంత్రం.ఆదేశము('cat stored.txt', ['saved-from-C'])
            ప్రమాణం['restore'] = యంత్రం.లాగ్_వరుస.decode('utf-8', 'replace')
        finally:
            యంత్రం.మూసివేయి()
        డేటా = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', డేటా, (1 + సూచీ * 259) * 512 + 4)[0] for సూచీ in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        డేటా[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(డేటా)
        యంత్రం = వర్చువల్_యంత్రం(స్థానము / 'build/kernel.elf', 저장매체=매체)
        try:
            యంత్రం.ఆదేశము('cat note.txt', ['generation-one'])
            యంత్రం.ఆదేశము('cat stored.txt', ['saved-from-C'])
            ప్రమాణం['checksum_fallback'] = యంత్రం.లాగ్_వరుస.decode('utf-8', 'replace')
        finally:
            యంత్రం.మూసివేయి()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        యంత్రం = వర్చువల్_యంత్రం(స్థానము / 'build/kernel.elf', 저장매체=다른매체)
        try:
            యంత్రం.ఆదేశము('sync', ['Sync: -19'])
        finally:
            యంత్రం.మూసివేయి()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        ప్రమాణం['foreign_disk_unchanged'] = True
    (స్థానము / 'build/보존시험.json').write_text(json.dumps(ప్రమాణం, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE నిల్వ_మూల్యం/ISO 재부팅/검사합 పునరుద్ధరణ_స్థితి/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    అమలు_చేయి_ఆదేశం()
