#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

Положај = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as 임시:
    именик_вриједност = Path(임시)
    경계 = именик_вриједност / '시험장치.java'
    경계.write_text('''
class уређај_вриједност { static int временска_ознака_вриједност; static int 밀리초() { return временска_ознака_вриједност++; } static void 잠시양보() {} }
class Текст_Терминал { static void Пише(String вриједност) {} static void 수쓰기(int вриједност) {} }
class Мрежа_драјвер_уређаја {
    static int 입출력기준주소 = 1, 송신수, 수신수;
    static int[] уређај_адреса = {0x52,0x54,0,0x12,0x34,0x56}, недавно_вриједност;
    static int 받기(int[] подаци) { return 0; }
    static int послати(int[] подаци, int дужина_вриједност) { недавно_вриједност = подаци.clone(); return дужина_вриједност; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(именик_вриједност), str(경계),
                    str(Положај / 'ИЗВОР/Мрежа_комплет.java'), str(Положај / '시험/패킷시험.java')], check=True)
    subprocess.run(['java', '-cp', str(именик_вриједност), '패킷시험'], check=True, timeout=10)
