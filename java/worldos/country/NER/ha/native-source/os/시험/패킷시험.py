#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    ma_ajiya_Daraja = Path(임시)
    경계 = ma_ajiya_Daraja / '시험장치.java'
    경계.write_text('''
class na_ura_Daraja { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void Yi_Rubutu(String Daraja) {} static void 수쓰기(int Daraja) {} }
class Hanyar_sadarwa_diraiba {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] na_ura_imel = {0x52,0x54,0,0x12,0x34,0x56}, na_kwanan_nan_Daraja;
    static int 받기(int[] Tarin_bayani) { return 0; }
    static int Aika(int[] Tarin_bayani, int Tsawo_Daraja) { na_kwanan_nan_Daraja = Tarin_bayani.clone(); return Tsawo_Daraja; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(ma_ajiya_Daraja), str(경계),
                    str(위치 / 'tushe/Hanyar_sadarwa_tara.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(ma_ajiya_Daraja), '패킷시험'], check=True, timeout=10)
