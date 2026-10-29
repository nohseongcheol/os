#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import sethalwa_motšhene, 위치
from 자바시험 import rulaganya_boleng, moeng_faele

def phethagatša_taelo():
    결과 = {}
    mohlodi = (위치.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        motšhene = sethalwa_motšhene(위치 / ('build/kernel.' + 종류), 종류, Netweke_boleng=False)
        try:
            rulaganya_boleng(motšhene, 'FileDemo.java', mohlodi)
            motšhene.Taelo('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for poeletšo_boleng in range(2):
                출력 = motšhene.Taelo('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            go_tsenya_tshedimošo_Lenaneo = motšhene.Taelo('ls', ['java.txt  3 bytes'])
            Bogolo = int(re.search(r'FileDemo.class\s+(\d+) bytes', go_tsenya_tshedimošo_Lenaneo)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                lelokelelo_boleng = Path(임시)
                moeng_faele(motšhene, 2, Bogolo, lelokelelo_boleng / 'FileDemo.class')
                go_nea_ditirelo = subprocess.check_output(['java', '-Xverify:all', '-cp', str(lelokelelo_boleng), 'FileDemo'], cwd=str(lelokelelo_boleng), universal_newlines=True)
                assert go_nea_ditirelo == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', go_nea_ditirelo
                assert (lelokelelo_boleng / 'java.txt').read_bytes() == b'A\xffB'
            rulaganya_boleng(motšhene, 'FileDemo.java', mohlodi.replace('output.write(65);', 'output.close(); output.write(65);'))
            motšhene.Taelo('javac FileDemo.java', ['Exit: 0'])
            motšhene.Taelo('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            rulaganya_boleng(motšhene, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            motšhene.Taelo('javac FileDemo.java', ['Exit: 0'])
            motšhene.Taelo('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            motšhene.Taelo('run hello recovered', ['Exit: 0'])
            결과[종류] = motšhene.pego_rei.decode('utf-8', 'replace')
        finally:
            motšhene.Tswalela()
        print('PASS:', 종류, '게스트 Java Faele 생성/이어쓰기/paete_boleng/EOF/닫힘/go_palelwa_boleng/OpenJDK 교차 phethagatša_taelo', flush=True)
    (위치 / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    phethagatša_taelo()
