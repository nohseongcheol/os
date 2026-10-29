#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Posisie = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    gids_VALUE = Path(임시)
    경계 = gids_VALUE / '시험장치.java'
    경계.write_text('''
class mobiel_VALUE { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class SMS_Terminaal { static void Skryf(String VALUE) {} static void 수쓰기(int VALUE) {} }
class Netwerk_drywer {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] mobiel_adres = {0x52,0x54,0,0x12,0x34,0x56}, onlangse_VALUE;
    static int 받기(int[] data) { return 0; }
    static int e_pos(int[] data, int lengte_VALUE) { onlangse_VALUE = data.clone(); return lengte_VALUE; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(gids_VALUE), str(경계),
                    str(Posisie / 'Bron/Netwerk_Stapel.java'), str(Posisie / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(gids_VALUE), '패킷시험'], check=True, timeout=10)
