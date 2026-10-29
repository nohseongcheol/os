#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import seka_motšhine, 위치
from 자바시험 import Tseleganya_Boleng, moeng_faele

def diragatsa_Taelo():
    결과 = {}
    Motswedi = (위치.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        motšhine = seka_motšhine(위치 / ('build/kernel.' + 종류), 종류, Neteweke_Boleng=False)
        try:
            Tseleganya_Boleng(motšhine, 'FileDemo.java', Motswedi)
            motšhine.Taelo('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for poeletso_Boleng in range(2):
                출력 = motšhine.Taelo('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            tsenyo_lenaane = motšhine.Taelo('ls', ['java.txt  3 bytes'])
            lekanya = int(re.search(r'FileDemo.class\s+(\d+) bytes', tsenyo_lenaane)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                Lenaneofaele_Boleng = Path(임시)
                moeng_faele(motšhine, 2, lekanya, Lenaneofaele_Boleng / 'FileDemo.class')
                pinagare = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Lenaneofaele_Boleng), 'FileDemo'], cwd=str(Lenaneofaele_Boleng), universal_newlines=True)
                assert pinagare == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', pinagare
                assert (Lenaneofaele_Boleng / 'java.txt').read_bytes() == b'A\xffB'
            Tseleganya_Boleng(motšhine, 'FileDemo.java', Motswedi.replace('output.write(65);', 'output.close(); output.write(65);'))
            motšhine.Taelo('javac FileDemo.java', ['Exit: 0'])
            motšhine.Taelo('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            Tseleganya_Boleng(motšhine, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            motšhine.Taelo('javac FileDemo.java', ['Exit: 0'])
            motšhine.Taelo('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            motšhine.Taelo('run hello recovered', ['Exit: 0'])
            결과[종류] = motšhine.rekota_mola.decode('utf-8', 'replace')
        finally:
            motšhine.tswala()
        print('PASS:', 종류, '게스트 Java faele 생성/이어쓰기/baete_Boleng/EOF/닫힘/palelo_Boleng/OpenJDK 교차 diragatsa_Taelo', flush=True)
    (위치 / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    diragatsa_Taelo()
