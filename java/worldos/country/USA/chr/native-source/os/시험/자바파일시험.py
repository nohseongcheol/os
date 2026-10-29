#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from ᎠᏓᎪᎵᏰᏍᎩ_ᎬᏗᏍᎩ_ᏧᎾᏚᏓᎵ import 가상기계, 위치
from 자바시험 import ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ, ᎠᏓᏩᏛᎯᏙᎯ_ᎠᏍᏆᏂᎪᏙᏗ

def ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ():
    결과 = {}
    ᎦᏟᏌᏅᎯ_0201f362 = (위치.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        기계 = 가상기계(위치 / ('build/kernel.' + 종류), 종류, ᏧᎾᏚᏓᎵ_ᏧᎬᏩᎶᏗᏯ=False)
        try:
            ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ(기계, 'FileDemo.java', ᎦᏟᏌᏅᎯ_0201f362)
            기계.ᎤᏁᏤᎸᎩ('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for 반복 in range(2):
                출력 = 기계.ᎤᏁᏤᎸᎩ('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ = 기계.ᎤᏁᏤᎸᎩ('ls', ['java.txt  3 bytes'])
            ᎢᎩᏓ = int(re.search(r'FileDemo.class\s+(\d+) bytes', Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ = Path(임시)
                ᎠᏓᏩᏛᎯᏙᎯ_ᎠᏍᏆᏂᎪᏙᏗ(기계, 2, ᎢᎩᏓ, ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'FileDemo.class')
                ᎠᏁᏢᏍᎩ = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ), 'FileDemo'], cwd=str(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ), universal_newlines=True)
                assert ᎠᏁᏢᏍᎩ == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', ᎠᏁᏢᏍᎩ
                assert (ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'java.txt').read_bytes() == b'A\xffB'
            ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ(기계, 'FileDemo.java', ᎦᏟᏌᏅᎯ_0201f362.replace('output.write(65);', 'output.close(); output.write(65);'))
            기계.ᎤᏁᏤᎸᎩ('javac FileDemo.java', ['Exit: 0'])
            기계.ᎤᏁᏤᎸᎩ('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ(기계, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            기계.ᎤᏁᏤᎸᎩ('javac FileDemo.java', ['Exit: 0'])
            기계.ᎤᏁᏤᎸᎩ('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            기계.ᎤᏁᏤᎸᎩ('run hello recovered', ['Exit: 0'])
            결과[종류] = 기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.decode('utf-8', 'replace')
        finally:
            기계.ᎯᏍᏚᎲᎦ()
        print('PASS:', 종류, '게스트 Java ᎠᏍᏆᏂᎪᏙᏗ 생성/이어쓰기/byte_ᏧᎬᏩᎶᏗᏯ/EOF/닫힘/ᎤᏄᎸᎲᎦ_ᏧᎬᏩᎶᏗᏯ/OpenJDK 교차 ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ', flush=True)
    (위치 / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
