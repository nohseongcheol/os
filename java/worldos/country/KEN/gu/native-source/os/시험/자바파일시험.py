#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import વર્ચુઅલ_મશીન, સ્થાન
from 자바시험 import સંપાદન_મૂલ્ય, અતિથિ_ફાઇલ

def અમલ_કરો_આદેશ():
    પરિમાણ = {}
    સ્રોત = (સ્થાન.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        મશીન = વર્ચુઅલ_મશીન(સ્થાન / ('build/kernel.' + 종류), 종류, નેટવર્ક_મૂલ્ય=False)
        try:
            સંપાદન_મૂલ્ય(મશીન, 'FileDemo.java', સ્રોત)
            મશીન.આદેશ('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for પુનરાવર્તન_મૂલ્ય in range(2):
                આઉટપુટ = મશીન.આદેશ('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            પ્રવેશ_સૂચી = મશીન.આદેશ('ls', ['java.txt  3 bytes'])
            માપ = int(re.search(r'FileDemo.class\s+(\d+) bytes', પ્રવેશ_સૂચી)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                નિર્દેશિકા_મૂલ્ય = Path(임시)
                અતિથિ_ફાઇલ(મશીન, 2, માપ, નિર્દેશિકા_મૂલ્ય / 'FileDemo.class')
                હોસ્ટ = subprocess.check_output(['java', '-Xverify:all', '-cp', str(નિર્દેશિકા_મૂલ્ય), 'FileDemo'], cwd=str(નિર્દેશિકા_મૂલ્ય), universal_newlines=True)
                assert હોસ્ટ == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', હોસ્ટ
                assert (નિર્દેશિકા_મૂલ્ય / 'java.txt').read_bytes() == b'A\xffB'
            સંપાદન_મૂલ્ય(મશીન, 'FileDemo.java', સ્રોત.replace('output.write(65);', 'output.close(); output.write(65);'))
            મશીન.આદેશ('javac FileDemo.java', ['Exit: 0'])
            મશીન.આદેશ('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            સંપાદન_મૂલ્ય(મશીન, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            મશીન.આદેશ('javac FileDemo.java', ['Exit: 0'])
            મશીન.આદેશ('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            મશીન.આદેશ('run hello recovered', ['Exit: 0'])
            પરિમાણ[종류] = મશીન.લૉગ_પંક્તિ.decode('utf-8', 'replace')
        finally:
            મશીન.બંધ_કરો()
        print('PASS:', 종류, '게스트 Java ફાઈલ જનરેટ_કરો/이어쓰기/બાઇટ_મૂલ્ય/EOF/닫힘/નિષ્ફળતા_મૂલ્ય/OpenJDK 교차 અમલ_કરો_આદેશ', flush=True)
    (સ્થાન / 'build/자바파일시험.json').write_text(json.dumps(પરિમાણ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    અમલ_કરો_આદેશ()
