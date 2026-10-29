#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import వర్చువల్_యంత్రం, స్థానము
from 자바시험 import సంకలనంచేయు_మూల్యం, అతిథి_ఫైలు

def అమలు_చేయి_ఆదేశం():
    ప్రమాణం = {}
    వనరు = (స్థానము.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        యంత్రం = వర్చువల్_యంత్రం(స్థానము / ('build/kernel.' + 종류), 종류, నెట్_వర్క్_మూల్యం=False)
        try:
            సంకలనంచేయు_మూల్యం(యంత్రం, 'FileDemo.java', వనరు)
            యంత్రం.ఆదేశము('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for పునరావృతం_మూల్యం in range(2):
                అవుట్పుట్ = యంత్రం.ఆదేశము('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            ప్రవేశం_జాబితా = యంత్రం.ఆదేశము('ls', ['java.txt  3 bytes'])
            పరిమాణం = int(re.search(r'FileDemo.class\s+(\d+) bytes', ప్రవేశం_జాబితా)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                సంచయని_మూల్యం = Path(임시)
                అతిథి_ఫైలు(యంత్రం, 2, పరిమాణం, సంచయని_మూల్యం / 'FileDemo.class')
                హోస్ట్ = subprocess.check_output(['java', '-Xverify:all', '-cp', str(సంచయని_మూల్యం), 'FileDemo'], cwd=str(సంచయని_మూల్యం), universal_newlines=True)
                assert హోస్ట్ == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', హోస్ట్
                assert (సంచయని_మూల్యం / 'java.txt').read_bytes() == b'A\xffB'
            సంకలనంచేయు_మూల్యం(యంత్రం, 'FileDemo.java', వనరు.replace('output.write(65);', 'output.close(); output.write(65);'))
            యంత్రం.ఆదేశము('javac FileDemo.java', ['Exit: 0'])
            యంత్రం.ఆదేశము('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            సంకలనంచేయు_మూల్యం(యంత్రం, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            యంత్రం.ఆదేశము('javac FileDemo.java', ['Exit: 0'])
            యంత్రం.ఆదేశము('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            యంత్రం.ఆదేశము('run hello recovered', ['Exit: 0'])
            ప్రమాణం[종류] = యంత్రం.లాగ్_వరుస.decode('utf-8', 'replace')
        finally:
            యంత్రం.మూసివేయి()
        print('PASS:', 종류, '게스트 Java దస్త్రం రూపొందించు/이어쓰기/బైట్_మూల్యం/EOF/닫힘/వైఫల్యం_మూల్యం/OpenJDK 교차 అమలు_చేయి_ఆదేశం', flush=True)
    (స్థానము / 'build/자바파일시험.json').write_text(json.dumps(ప్రమాణం, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    అమలు_చేయి_ఆదేశం()
