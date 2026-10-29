#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import مجازی_مشین

위치 = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('میڈیا_ٹول', 위치 / 'اوزار/بنڑاؤ_ذخیرہ_میڈیا.py')
میڈیا_ٹول = importlib.util.module_from_spec(명세)
명세.loader.exec_module(میڈیا_ٹول)

def تدوین_قدر(مشین, اجزاء_قدر):
    چلاؤ = len(مشین.لاگ_صف)
    مشین.직렬.sendall(('edit note.txt\n' + اجزاء_قدر + '\n.save\n').encode())
    return مشین.기다림('jkoros> ', چلاؤ)

def نفاذ_کرو_حکم():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        میڈیا_قدر = Path(임시) / 'files.img'
        میڈیا_ٹول.بنڑاؤ_داخلہ(میڈیا_قدر)
        مشین = مجازی_مشین(위치 / 'build/kernel.elf', 저장매체=میڈیا_قدر)
        try:
            مشین.حکم('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            تدوین_قدر(مشین, 'generation-one')
            مشین.حکم('sync', ['Sync: 0'])
            تدوین_قدر(مشین, 'generation-two')
            مشین.حکم('sync', ['Sync: 0'])
            تدوین_قدر(مشین, 'unsynced-three')
            결과['save'] = مشین.لاگ_صف.decode('utf-8', 'replace')
        finally:
            مشین.بند_کرو()
        مشین = مجازی_مشین(위치 / 'build/kernel.iso', 'iso', 저장매체=میڈیا_قدر)
        try:
            출력 = مشین.حکم('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            مشین.حکم('cat stored.txt', ['saved-from-C'])
            결과['restore'] = مشین.لاگ_صف.decode('utf-8', 'replace')
        finally:
            مشین.بند_کرو()
        کوائف = bytearray(میڈیا_قدر.read_bytes())
        세대들 = [struct.unpack_from('<I', کوائف, (1 + اشاریہ * 259) * 512 + 4)[0] for اشاریہ in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        کوائف[(1 + 최신 * 259 + 3) * 512] ^= 1
        میڈیا_قدر.write_bytes(کوائف)
        مشین = مجازی_مشین(위치 / 'build/kernel.elf', 저장매체=میڈیا_قدر)
        try:
            مشین.حکم('cat note.txt', ['generation-one'])
            مشین.حکم('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = مشین.لاگ_صف.decode('utf-8', 'replace')
        finally:
            مشین.بند_کرو()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        مشین = مجازی_مشین(위치 / 'build/kernel.elf', 저장매체=다른매체)
        try:
            مشین.حکم('sync', ['Sync: -19'])
        finally:
            مشین.بند_کرو()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (위치 / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE ذخیرہ_کرو_قدر/ISO 재부팅/검사합 بحال_کرنا_حالت/다른 میڈیا_قدر 비변경', flush=True)

if __name__ == '__main__':
    نفاذ_کرو_حکم()
