#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import kidafatika_imashini, 위치
from 자바시험 import guhindura_agaciro, 게스트파일

def gukora_ibwiriza():
    결과 = {}
    Inkomoko = (위치.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        imashini = kidafatika_imashini(위치 / ('build/kernel.' + 종류), 종류, Urusobemiyoboro_agaciro=False)
        try:
            guhindura_agaciro(imashini, 'FileDemo.java', Inkomoko)
            imashini.Icyo_wifuza('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for isubiramo_agaciro in range(2):
                출력 = imashini.Icyo_wifuza('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            icyinjizwa_Urutonde = imashini.Icyo_wifuza('ls', ['java.txt  3 bytes'])
            Ingano = int(re.search(r'FileDemo.class\s+(\d+) bytes', icyinjizwa_Urutonde)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                ububiko_agaciro_e5561a2b = Path(임시)
                게스트파일(imashini, 2, Ingano, ububiko_agaciro_e5561a2b / 'FileDemo.class')
                gucumbikira = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ububiko_agaciro_e5561a2b), 'FileDemo'], cwd=str(ububiko_agaciro_e5561a2b), universal_newlines=True)
                assert gucumbikira == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', gucumbikira
                assert (ububiko_agaciro_e5561a2b / 'java.txt').read_bytes() == b'A\xffB'
            guhindura_agaciro(imashini, 'FileDemo.java', Inkomoko.replace('output.write(65);', 'output.close(); output.write(65);'))
            imashini.Icyo_wifuza('javac FileDemo.java', ['Exit: 0'])
            imashini.Icyo_wifuza('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            guhindura_agaciro(imashini, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            imashini.Icyo_wifuza('javac FileDemo.java', ['Exit: 0'])
            imashini.Icyo_wifuza('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            imashini.Icyo_wifuza('run hello recovered', ['Exit: 0'])
            결과[종류] = imashini.kubika_umurongo.decode('utf-8', 'replace')
        finally:
            imashini.Gufunga()
        print('PASS:', 종류, '게스트 Java Idosiye 생성/이어쓰기/bayiti_agaciro/EOF/닫힘/kudakora_agaciro/OpenJDK 교차 gukora_ibwiriza', flush=True)
    (위치 / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    gukora_ibwiriza()
