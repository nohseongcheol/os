#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import виртуалӣ_компютер, 위치
from 자바시험 import таҳрир_қимат, меҳмон_файл

def иҷро_кардан_фармон():
    결과 = {}
    манбаъ = (위치.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        компютер = виртуалӣ_компютер(위치 / ('build/kernel.' + 종류), 종류, Шабака_қимат=False)
        try:
            таҳрир_қимат(компютер, 'FileDemo.java', манбаъ)
            компютер.фармон('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for такрор_қимат in range(2):
                출력 = компютер.фармон('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            ворида_Рӯйхат = компютер.фармон('ls', ['java.txt  3 bytes'])
            андоза_кардан = int(re.search(r'FileDemo.class\s+(\d+) bytes', ворида_Рӯйхат)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                директория_қимат = Path(임시)
                меҳмон_файл(компютер, 2, андоза_кардан, директория_қимат / 'FileDemo.class')
                мизбон = subprocess.check_output(['java', '-Xverify:all', '-cp', str(директория_қимат), 'FileDemo'], cwd=str(директория_қимат), universal_newlines=True)
                assert мизбон == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', мизбон
                assert (директория_қимат / 'java.txt').read_bytes() == b'A\xffB'
            таҳрир_қимат(компютер, 'FileDemo.java', манбаъ.replace('output.write(65);', 'output.close(); output.write(65);'))
            компютер.фармон('javac FileDemo.java', ['Exit: 0'])
            компютер.фармон('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            таҳрир_қимат(компютер, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            компютер.фармон('javac FileDemo.java', ['Exit: 0'])
            компютер.фармон('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            компютер.фармон('run hello recovered', ['Exit: 0'])
            결과[종류] = компютер.сабт_кардан_сабт.decode('utf-8', 'replace')
        finally:
            компютер.Пӯшидан()
        print('PASS:', 종류, '게스트 Java Файл 생성/이어쓰기/байт_қимат/EOF/닫힘/нокомӣ_қимат/OpenJDK 교차 иҷро_кардан_фармон', flush=True)
    (위치 / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    иҷро_кардан_фармон()
