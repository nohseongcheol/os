#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import ਵਰਚੁਅਲ_ਮਸ਼ੀਨ, ਸਥਿਤੀ
from 자바시험 import ਸੰਪਾਦਨ_ਕੀਮਤ, ਗੈਸਟ_ਲਿਖਤ_ਪੱਤਰ

def ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼():
    ਮਾਪ = {}
    ਸਰੋਤ = (ਸਥਿਤੀ.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        ਮਸ਼ੀਨ = ਵਰਚੁਅਲ_ਮਸ਼ੀਨ(ਸਥਿਤੀ / ('build/kernel.' + 종류), 종류, ਨੈਟਵਰਕ_ਕੀਮਤ=False)
        try:
            ਸੰਪਾਦਨ_ਕੀਮਤ(ਮਸ਼ੀਨ, 'FileDemo.java', ਸਰੋਤ)
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for ਦੋਹਰਾਵ_ਕੀਮਤ in range(2):
                ਆਉਟਪੁੱਟ = ਮਸ਼ੀਨ.ਕਮਾਂਡ('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            ਦਾਖਲਾ_ਸੂਚੀ = ਮਸ਼ੀਨ.ਕਮਾਂਡ('ls', ['java.txt  3 bytes'])
            ਆਕਾਰ = int(re.search(r'FileDemo.class\s+(\d+) bytes', ਦਾਖਲਾ_ਸੂਚੀ)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ = Path(임시)
                ਗੈਸਟ_ਲਿਖਤ_ਪੱਤਰ(ਮਸ਼ੀਨ, 2, ਆਕਾਰ, ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'FileDemo.class')
                ਹੋਸਟ = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ), 'FileDemo'], cwd=str(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ), universal_newlines=True)
                assert ਹੋਸਟ == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', ਹੋਸਟ
                assert (ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'java.txt').read_bytes() == b'A\xffB'
            ਸੰਪਾਦਨ_ਕੀਮਤ(ਮਸ਼ੀਨ, 'FileDemo.java', ਸਰੋਤ.replace('output.write(65);', 'output.close(); output.write(65);'))
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('javac FileDemo.java', ['Exit: 0'])
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            ਸੰਪਾਦਨ_ਕੀਮਤ(ਮਸ਼ੀਨ, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('javac FileDemo.java', ['Exit: 0'])
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('run hello recovered', ['Exit: 0'])
            ਮਾਪ[종류] = ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ.decode('utf-8', 'replace')
        finally:
            ਮਸ਼ੀਨ.ਬੰਦ_ਕਰੋ()
        print('PASS:', 종류, '게스트 Java ਫਾਇਲ ਜਨਰੇਟ_ਕਰੋ/이어쓰기/ਬਾਈਟ_ਕੀਮਤ/EOF/닫힘/ਅਸਫਲ_ਕੀਮਤ/OpenJDK 교차 ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼', flush=True)
    (ਸਥਿਤੀ / 'build/자바파일시험.json').write_text(json.dumps(ਮਾਪ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
