#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import utalagu_umshini, 위치
from 자바시험 import hlela_inani, isivakashi_ifayela

def yenza_umyalo():
    결과 = {}
    umthombo = (위치.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        umshini = utalagu_umshini(위치 / ('build/kernel.' + 종류), 종류, iNethiwekhi_inani=False)
        try:
            hlela_inani(umshini, 'FileDemo.java', umthombo)
            umshini.Umlayelo('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for impinda_inani in range(2):
                출력 = umshini.Umlayelo('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            okufakwayo_Uhlu = umshini.Umlayelo('ls', ['java.txt  3 bytes'])
            Ubungako = int(re.search(r'FileDemo.class\s+(\d+) bytes', okufakwayo_Uhlu)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                umkhombandlela_inani = Path(임시)
                isivakashi_ifayela(umshini, 2, Ubungako, umkhombandlela_inani / 'FileDemo.class')
                singatha = subprocess.check_output(['java', '-Xverify:all', '-cp', str(umkhombandlela_inani), 'FileDemo'], cwd=str(umkhombandlela_inani), universal_newlines=True)
                assert singatha == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', singatha
                assert (umkhombandlela_inani / 'java.txt').read_bytes() == b'A\xffB'
            hlela_inani(umshini, 'FileDemo.java', umthombo.replace('output.write(65);', 'output.close(); output.write(65);'))
            umshini.Umlayelo('javac FileDemo.java', ['Exit: 0'])
            umshini.Umlayelo('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            hlela_inani(umshini, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            umshini.Umlayelo('javac FileDemo.java', ['Exit: 0'])
            umshini.Umlayelo('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            umshini.Umlayelo('run hello recovered', ['Exit: 0'])
            결과[종류] = umshini.loga_umugqa.decode('utf-8', 'replace')
        finally:
            umshini.Vala()
        print('PASS:', 종류, '게스트 Java Ihele 생성/이어쓰기/ibhayithi_inani/EOF/닫힘/ukwehluleka_inani/OpenJDK 교차 yenza_umyalo', flush=True)
    (위치 / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    yenza_umyalo()
