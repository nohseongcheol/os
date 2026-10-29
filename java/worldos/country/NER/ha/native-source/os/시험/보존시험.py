#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import Mai_alaka_da_aikin_na_ura_na_boye_na_ura_mai_kwakwalwa

위치 = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('Midiya_kayan_aiki', 위치 / 'Kaya/ƙirƙíra_Wurin_adana_Midiya.py')
Midiya_kayan_aiki = importlib.util.module_from_spec(명세)
명세.loader.exec_module(Midiya_kayan_aiki)

def gyaran_Daraja(na_ura_mai_kwakwalwa, kunshiya_Daraja):
    Tafiyar_da = len(na_ura_mai_kwakwalwa.logu_naɗa)
    na_ura_mai_kwakwalwa.직렬.sendall(('edit note.txt\n' + kunshiya_Daraja + '\n.save\n').encode())
    return na_ura_mai_kwakwalwa.jira_Matsayi('jkoros> ', Tafiyar_da)

def gudanar_Umarni():
    결과 = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        Midiya_Daraja = Path(임시) / 'files.img'
        Midiya_kayan_aiki.ƙirƙíra_Mashigar_bayanai(Midiya_Daraja)
        na_ura_mai_kwakwalwa = Mai_alaka_da_aikin_na_ura_na_boye_na_ura_mai_kwakwalwa(위치 / 'build/kernel.elf', 저장매체=Midiya_Daraja)
        try:
            na_ura_mai_kwakwalwa.Umarni('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            gyaran_Daraja(na_ura_mai_kwakwalwa, 'generation-one')
            na_ura_mai_kwakwalwa.Umarni('sync', ['Sync: 0'])
            gyaran_Daraja(na_ura_mai_kwakwalwa, 'generation-two')
            na_ura_mai_kwakwalwa.Umarni('sync', ['Sync: 0'])
            gyaran_Daraja(na_ura_mai_kwakwalwa, 'unsynced-three')
            결과['save'] = na_ura_mai_kwakwalwa.logu_naɗa.decode('utf-8', 'replace')
        finally:
            na_ura_mai_kwakwalwa.Rufe()
        na_ura_mai_kwakwalwa = Mai_alaka_da_aikin_na_ura_na_boye_na_ura_mai_kwakwalwa(위치 / 'build/kernel.iso', 'iso', 저장매체=Midiya_Daraja)
        try:
            출력 = na_ura_mai_kwakwalwa.Umarni('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in 출력
            na_ura_mai_kwakwalwa.Umarni('cat stored.txt', ['saved-from-C'])
            결과['restore'] = na_ura_mai_kwakwalwa.logu_naɗa.decode('utf-8', 'replace')
        finally:
            na_ura_mai_kwakwalwa.Rufe()
        Tarin_bayani = bytearray(Midiya_Daraja.read_bytes())
        세대들 = [struct.unpack_from('<I', Tarin_bayani, (1 + Indes * 259) * 512 + 4)[0] for Indes in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        Tarin_bayani[(1 + 최신 * 259 + 3) * 512] ^= 1
        Midiya_Daraja.write_bytes(Tarin_bayani)
        na_ura_mai_kwakwalwa = Mai_alaka_da_aikin_na_ura_na_boye_na_ura_mai_kwakwalwa(위치 / 'build/kernel.elf', 저장매체=Midiya_Daraja)
        try:
            na_ura_mai_kwakwalwa.Umarni('cat note.txt', ['generation-one'])
            na_ura_mai_kwakwalwa.Umarni('cat stored.txt', ['saved-from-C'])
            결과['checksum_fallback'] = na_ura_mai_kwakwalwa.logu_naɗa.decode('utf-8', 'replace')
        finally:
            na_ura_mai_kwakwalwa.Rufe()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        na_ura_mai_kwakwalwa = Mai_alaka_da_aikin_na_ura_na_boye_na_ura_mai_kwakwalwa(위치 / 'build/kernel.elf', 저장매체=다른매체)
        try:
            na_ura_mai_kwakwalwa.Umarni('sync', ['Sync: -19'])
        finally:
            na_ura_mai_kwakwalwa.Rufe()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        결과['foreign_disk_unchanged'] = True
    (위치 / 'build/보존시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Ajiye_Daraja/ISO 재부팅/checksum dawo_da_martaba_Matsayi/다른 Midiya_Daraja 비변경', flush=True)

if __name__ == '__main__':
    gudanar_Umarni()
