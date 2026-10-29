#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import enembonakalo_yenyani_umatshini, 위치
from 자바시험 import hlela_ixabiso, undwendwe_ifayile

def ukwenza_umyalelo():
    결과 = {}
    UMTHOMBO = (위치.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        umatshini = enembonakalo_yenyani_umatshini(위치 / ('build/kernel.' + 종류), 종류, Inethiwekhi_ixabiso=False)
        try:
            hlela_ixabiso(umatshini, 'FileDemo.java', UMTHOMBO)
            umatshini.Umyalelo('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for uniko_lomyalelo_omnye_ixabiso in range(2):
                출력 = umatshini.Umyalelo('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            ufako_nkcukacha_uludwe = umatshini.Umyalelo('ls', ['java.txt  3 bytes'])
            Ubukhulu = int(re.search(r'FileDemo.class\s+(\d+) bytes', ufako_nkcukacha_uludwe)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                isalathisi_ixabiso_e5561a2b = Path(임시)
                undwendwe_ifayile(umatshini, 2, Ubukhulu, isalathisi_ixabiso_e5561a2b / 'FileDemo.class')
                umsingathi = subprocess.check_output(['java', '-Xverify:all', '-cp', str(isalathisi_ixabiso_e5561a2b), 'FileDemo'], cwd=str(isalathisi_ixabiso_e5561a2b), universal_newlines=True)
                assert umsingathi == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', umsingathi
                assert (isalathisi_ixabiso_e5561a2b / 'java.txt').read_bytes() == b'A\xffB'
            hlela_ixabiso(umatshini, 'FileDemo.java', UMTHOMBO.replace('output.write(65);', 'output.close(); output.write(65);'))
            umatshini.Umyalelo('javac FileDemo.java', ['Exit: 0'])
            umatshini.Umyalelo('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            hlela_ixabiso(umatshini, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            umatshini.Umyalelo('javac FileDemo.java', ['Exit: 0'])
            umatshini.Umyalelo('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            umatshini.Umyalelo('run hello recovered', ['Exit: 0'])
            결과[종류] = umatshini.ilog_umqolo.decode('utf-8', 'replace')
        finally:
            umatshini.Vala()
        print('PASS:', 종류, '게스트 Java iFayili 생성/이어쓰기/ibhayithi_ixabiso/EOF/닫힘/ukungaphumeleli_ixabiso/OpenJDK 교차 ukwenza_umyalelo', flush=True)
    (위치 / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ukwenza_umyalelo()
