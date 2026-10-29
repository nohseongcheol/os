#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Asukoht = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    kaust_VALUE = Path(임시)
    경계 = kaust_VALUE / '시험장치.java'
    경계.write_text('''
class seade_VALUE { static int ajatempel_VALUE; static int 밀리초() { return ajatempel_VALUE++; } static void 잠시양보() {} }
class SMS_terminal { static void Kirjutamine(String VALUE) {} static void kirjutamine_number(int VALUE) {} }
class võrk_draiver {
    static int 입출력기준주소 = 1, 송신수, saama_COUNT;
    static int[] seade_ADDRESS = {0x52,0x54,0,0x12,0x34,0x56}, hiljutised_VALUE;
    static int saama(int[] andmed) { return 0; }
    static int saatma(int[] andmed, int 길이) { hiljutised_VALUE = andmed.clone(); return 길이; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(kaust_VALUE), str(경계),
                    str(Asukoht / 'ALLIKAS/võrk_Virn.java'), str(Asukoht / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(kaust_VALUE), '패킷시험'], check=True, timeout=10)
