#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import ବାସ୍ତବ_ମେସିନ୍

ଅବସ୍ଥାନ = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('매체도구', ଅବସ୍ଥାନ / 'ଉପକରଣସମୂହ/저장매체만들기.py')
매체도구 = importlib.util.module_from_spec(명세)
명세.loader.exec_module(매체도구)

def ସଂପାଦନା_ମୂଲ୍ୟ(ମେସିନ୍, ବିଷୟ_ମୂଲ୍ୟ):
    ଚଳାନ୍ତୁ = len(ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି)
    ମେସିନ୍.직렬.sendall(('edit note.txt\n' + ବିଷୟ_ମୂଲ୍ୟ + '\n.save\n').encode())
    return ମେସିନ୍.ଅପେକ୍ଷା_ସ୍ଥିତି('jkoros> ', ଚଳାନ୍ତୁ)

def ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ():
    ମାପ = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        매체 = Path(임시) / 'files.img'
        매체도구.ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି(매체)
        ମେସିନ୍ = ବାସ୍ତବ_ମେସିନ୍(ଅବସ୍ଥାନ / 'build/kernel.elf', 저장매체=매체)
        try:
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            ସଂପାଦନା_ମୂଲ୍ୟ(ମେସିନ୍, 'generation-one')
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('sync', ['Sync: 0'])
            ସଂପାଦନା_ମୂଲ୍ୟ(ମେସିନ୍, 'generation-two')
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('sync', ['Sync: 0'])
            ସଂପାଦନା_ମୂଲ୍ୟ(ମେସିନ୍, 'unsynced-three')
            ମାପ['save'] = ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି.decode('utf-8', 'replace')
        finally:
            ମେସିନ୍.ବନ୍ଦ_କରନ୍ତୁ()
        ମେସିନ୍ = ବାସ୍ତବ_ମେସିନ୍(ଅବସ୍ଥାନ / 'build/kernel.iso', 'iso', 저장매체=매체)
        try:
            ନିର୍ଗମ = ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in ନିର୍ଗମ
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('cat stored.txt', ['saved-from-C'])
            ମାପ['restore'] = ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି.decode('utf-8', 'replace')
        finally:
            ମେସିନ୍.ବନ୍ଦ_କରନ୍ତୁ()
        ଡାଟା = bytearray(매체.read_bytes())
        세대들 = [struct.unpack_from('<I', ଡାଟା, (1 + ଅନୁକ୍ରମଣିକା * 259) * 512 + 4)[0] for ଅନୁକ୍ରମଣିକା in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        ଡାଟା[(1 + 최신 * 259 + 3) * 512] ^= 1
        매체.write_bytes(ଡାଟା)
        ମେସିନ୍ = ବାସ୍ତବ_ମେସିନ୍(ଅବସ୍ଥାନ / 'build/kernel.elf', 저장매체=매체)
        try:
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('cat note.txt', ['generation-one'])
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('cat stored.txt', ['saved-from-C'])
            ମାପ['checksum_fallback'] = ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି.decode('utf-8', 'replace')
        finally:
            ମେସିନ୍.ବନ୍ଦ_କରନ୍ତୁ()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        ମେସିନ୍ = ବାସ୍ତବ_ମେସିନ୍(ଅବସ୍ଥାନ / 'build/kernel.elf', 저장매체=다른매체)
        try:
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('sync', ['Sync: -19'])
        finally:
            ମେସିନ୍.ବନ୍ଦ_କରନ୍ତୁ()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        ମାପ['foreign_disk_unchanged'] = True
    (ଅବସ୍ଥାନ / 'build/보존시험.json').write_text(json.dumps(ମାପ, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ/ISO 재부팅/ଚେକସୁମ୍ ପୁନଃଉଦ୍ଧାର_କରିବା_ସ୍ଥିତି/다른 매체 비변경', flush=True)

if __name__ == '__main__':
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()
