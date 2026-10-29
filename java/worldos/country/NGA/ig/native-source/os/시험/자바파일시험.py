#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import kendìnuchè_ngwa_komputa, 위치
from 자바시험 import dezìmà_valuu, 게스트파일

def mee_nnyemiwu():
    결과 = {}
    ebensìbịa = (위치.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        ngwa_komputa = kendìnuchè_ngwa_komputa(위치 / ('build/kernel.' + 종류), 종류, Netwọọkụ_valuu=False)
        try:
            dezìmà_valuu(ngwa_komputa, 'FileDemo.java', ebensìbịa)
            ngwa_komputa.Ntiiwu('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for memmekwa_valuu in range(2):
                출력 = ngwa_komputa.Ntiiwu('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            ndebà_ndepụta = ngwa_komputa.Ntiiwu('ls', ['java.txt  3 bytes'])
            Ụhara = int(re.search(r'FileDemo.class\s+(\d+) bytes', ndebà_ndepụta)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                dàịrektrị_valuu = Path(임시)
                게스트파일(ngwa_komputa, 2, Ụhara, dàịrektrị_valuu / 'FileDemo.class')
                usu = subprocess.check_output(['java', '-Xverify:all', '-cp', str(dàịrektrị_valuu), 'FileDemo'], cwd=str(dàịrektrị_valuu), universal_newlines=True)
                assert usu == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', usu
                assert (dàịrektrị_valuu / 'java.txt').read_bytes() == b'A\xffB'
            dezìmà_valuu(ngwa_komputa, 'FileDemo.java', ebensìbịa.replace('output.write(65);', 'output.close(); output.write(65);'))
            ngwa_komputa.Ntiiwu('javac FileDemo.java', ['Exit: 0'])
            ngwa_komputa.Ntiiwu('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            dezìmà_valuu(ngwa_komputa, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            ngwa_komputa.Ntiiwu('javac FileDemo.java', ['Exit: 0'])
            ngwa_komputa.Ntiiwu('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            ngwa_komputa.Ntiiwu('run hello recovered', ['Exit: 0'])
            결과[종류] = ngwa_komputa.ndekọ_NDEKỌ.decode('utf-8', 'replace')
        finally:
            ngwa_komputa.Mechie()
        print('PASS:', 종류, '게스트 Java Faịlụ 생성/이어쓰기/baịtị_valuu/EOF/닫힘/ọdịdà_valuu/OpenJDK 교차 mee_nnyemiwu', flush=True)
    (위치 / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    mee_nnyemiwu()
