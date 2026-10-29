#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

위치 = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    лавлах_утга = Path(임시)
    경계 = лавлах_утга / '시험장치.java'
    경계.write_text('''
class гар_утас_утга { static int 시각; static int 밀리초() { return 시각++; } static void 잠시양보() {} }
class 문자단말 { static void Бичих(String утга) {} static void 수쓰기(int утга) {} }
class Сүлжээ_драйвер {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] гар_утас_хаяг = {0x52,0x54,0,0x12,0x34,0x56}, саяхны_үйлдлүүд_утга;
    static int 받기(int[] өгөгдөл) { return 0; }
    static int илгээх(int[] өгөгдөл, int урт_утга) { саяхны_үйлдлүүд_утга = өгөгдөл.clone(); return урт_утга; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(лавлах_утга), str(경계),
                    str(위치 / 'ЭХ/Сүлжээ_давхцал.java'), str(위치 / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(лавлах_утга), '패킷시험'], check=True, timeout=10)
