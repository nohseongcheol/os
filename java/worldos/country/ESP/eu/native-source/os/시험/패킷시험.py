#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Posizioa = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    direktorio_balio = Path(임시)
    경계 = direktorio_balio / '시험장치.java'
    경계.write_text('''
class gailu_balio { static int denbora_zigilu_balio; static int 밀리초() { return denbora_zigilu_balio++; } static void 잠시양보() {} }
class SMS_Terminal { static void Idatzi(String balio) {} static void 수쓰기(int balio) {} }
class sare_kontrolatzaile {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] gailu_helbide_856320c2 = {0x52,0x54,0,0x12,0x34,0x56}, azkenak_balio;
    static int 받기(int[] datuak) { return 0; }
    static int bidali(int[] datuak, int luzera_balio) { azkenak_balio = datuak.clone(); return luzera_balio; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(direktorio_balio), str(경계),
                    str(Posizioa / 'ITURBURUA/sare_pila.java'), str(Posizioa / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(direktorio_balio), '패킷시험'], check=True, timeout=10)
