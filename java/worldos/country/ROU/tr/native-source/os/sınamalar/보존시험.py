#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from test_kullanıcı_ağ import VM

konum = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('Medya_araç', konum / 'araçlar/açmak_Depolama_Medya.py')
Medya_araç = importlib.util.module_from_spec(명세)
명세.loader.exec_module(Medya_araç)

def Düzenle_değer(makine, içerik_değer):
    çalıştır = len(makine.LOG_KAYIT)
    makine.직렬.sendall(('edit note.txt\n' + içerik_değer + '\n.save\n').encode())
    return makine.bekleme_durumu('jkoros> ', çalıştır)

def yürütmek_komut():
    sonuç = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        Medya_değer = Path(임시) / 'files.img'
        Medya_araç.açmak_girdi(Medya_değer)
        makine = VM(konum / 'build/kernel.elf', Depolama_Orta=Medya_değer)
        try:
            makine.komut('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            Düzenle_değer(makine, 'generation-one')
            makine.komut('sync', ['Sync: 0'])
            Düzenle_değer(makine, 'generation-two')
            makine.komut('sync', ['Sync: 0'])
            Düzenle_değer(makine, 'unsynced-three')
            sonuç['save'] = makine.LOG_KAYIT.decode('utf-8', 'replace')
        finally:
            makine.Kapat()
        makine = VM(konum / 'build/kernel.iso', 'iso', Depolama_Orta=Medya_değer)
        try:
            metinÇıktısı = makine.komut('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in metinÇıktısı
            makine.komut('cat stored.txt', ['saved-from-C'])
            sonuç['restore'] = makine.LOG_KAYIT.decode('utf-8', 'replace')
        finally:
            makine.Kapat()
        veri = bytearray(Medya_değer.read_bytes())
        세대들 = [struct.unpack_from('<I', veri, (1 + Dizin * 259) * 512 + 4)[0] for Dizin in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        veri[(1 + 최신 * 259 + 3) * 512] ^= 1
        Medya_değer.write_bytes(veri)
        makine = VM(konum / 'build/kernel.elf', Depolama_Orta=Medya_değer)
        try:
            makine.komut('cat note.txt', ['generation-one'])
            makine.komut('cat stored.txt', ['saved-from-C'])
            sonuç['checksum_fallback'] = makine.LOG_KAYIT.decode('utf-8', 'replace')
        finally:
            makine.Kapat()
        Diğer_Medya = Path(임시) / 'foreign.img'
        Diğer_Medya.write_bytes(bytes([0x5a]) * (2048 * 512))
        Önceki_öğe = hashlib.sha256(Diğer_Medya.read_bytes()).hexdigest()
        makine = VM(konum / 'build/kernel.elf', Depolama_Orta=Diğer_Medya)
        try:
            makine.komut('sync', ['Sync: -19'])
        finally:
            makine.Kapat()
        assert hashlib.sha256(Diğer_Medya.read_bytes()).hexdigest() == Önceki_öğe
        sonuç['foreign_disk_unchanged'] = True
    (konum / 'build/보존시험.json').write_text(json.dumps(sonuç, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE depo_değer/ISO 재부팅/sağlama_toplamı kurtarmak_Durum/다른 Medya_değer 비변경', flush=True)

if __name__ == '__main__':
    yürütmek_komut()
