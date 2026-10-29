#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import និម្មិត_ម៉ាស៊ីន

កំណត់ទីតាំង = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', កំណត់ទីតាំង / 'ឧបករណ៍/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def កែសម្រួល_តំលៃ(ម៉ាស៊ីន, មាតិកា_តំលៃ):
    រត់ = len(ម៉ាស៊ីន.កំណត់_ហេតុ_ថត)
    ម៉ាស៊ីន.직렬.sendall(('edit note.txt\n' + មាតិកា_តំលៃ + '\n.save\n').encode())
    return ម៉ាស៊ីន.រង់ចាំ_ភាព('jkoros> ', រត់)

def អនុវត្ត_ពាក្យបញ្ជា():
    ការវាស់វែង = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.បង្កើត_ការបញ្ចូល(매체)
        ម៉ាស៊ីន = និម្មិត_ម៉ាស៊ីន(កំណត់ទីតាំង / 'build/kernel.elf', 저장매체=매체)
        try:
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            កែសម្រួល_តំលៃ(ម៉ាស៊ីន, 'generation-one')
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('sync', ['Sync: 0'])
            កែសម្រួល_តំលៃ(ម៉ាស៊ីន, 'generation-two')
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('sync', ['Sync: 0'])
            កែសម្រួល_តំលៃ(ម៉ាស៊ីន, 'unsynced-three')
            ការវាស់វែង['save'] = ម៉ាស៊ីន.កំណត់_ហេតុ_ថត.decode('utf-8', 'replace')
        finally:
            ម៉ាស៊ីន.បិទ()
        ម៉ាស៊ីន = និម្មិត_ម៉ាស៊ីន(កំណត់ទីតាំង / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            លទ្ធផល = ម៉ាស៊ីន.ពាក្យ_បញ្ជា('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in លទ្ធផល
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('cat stored.txt', ['saved-from-C'])
            ការវាស់វែង['restore'] = ម៉ាស៊ីន.កំណត់_ហេតុ_ថត.decode('utf-8', 'replace')
        finally:
            ម៉ាស៊ីន.បិទ()
        ទិន្នន័យ = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', ទិន្នន័យ, (1 + សន្ទស្សន៏ * 259) * 512 + 4)[0] for សន្ទស្សន៏ in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        ទិន្នន័យ[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(ទិន្នន័យ)
        ម៉ាស៊ីន = និម្មិត_ម៉ាស៊ីន(កំណត់ទីតាំង / 'build/kernel.elf', 저장매체=매체)
        try:
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('cat note.txt', ['generation-one'])
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('cat stored.txt', ['saved-from-C'])
            ការវាស់វែង['checksum_fallback'] = ម៉ាស៊ីន.កំណត់_ហេតុ_ថត.decode('utf-8', 'replace')
        finally:
            ម៉ាស៊ីន.បិទ()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        ម៉ាស៊ីន = និម្មិត_ម៉ាស៊ីន(កំណត់ទីតាំង / 'build/kernel.elf', 저장매체=다른매체)
        try:
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('sync', ['Sync: -19'])
        finally:
            ម៉ាស៊ីន.បិទ()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        ការវាស់វែង['foreign_disk_unchanged'] = True
    (កំណត់ទីតាំង / 'build/보존시험.json').write_text(json.dumps(ការវាស់វែង, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE ផ្ទុក_តំលៃ/ISO 재부팅/លេខសរុបដើម្បីពិនិត្យមើលទិន្នន័យត្រឹមត្រូវ សង្គ្រោះឯកសារ_ភាព/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    អនុវត្ត_ពាក្យបញ្ជា()
