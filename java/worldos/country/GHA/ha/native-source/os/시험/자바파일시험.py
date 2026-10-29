#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import Mai_alaka_da_aikin_na_ura_na_boye_na_ura_mai_kwakwalwa, 위치
from 자바시험 import gyaran_Daraja, baƙo_Fayil

def gudanar_Umarni():
    결과 = {}
    tushe = (위치.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        na_ura_mai_kwakwalwa = Mai_alaka_da_aikin_na_ura_na_boye_na_ura_mai_kwakwalwa(위치 / ('build/kernel.' + 종류), 종류, Hanyar_sadarwa_Daraja=False)
        try:
            gyaran_Daraja(na_ura_mai_kwakwalwa, 'FileDemo.java', tushe)
            na_ura_mai_kwakwalwa.Umarni('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sifirint_Daraja in range(2):
                출력 = na_ura_mai_kwakwalwa.Umarni('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            Mashigar_bayanai_Jeri = na_ura_mai_kwakwalwa.Umarni('ls', ['java.txt  3 bytes'])
            Girma = int(re.search(r'FileDemo.class\s+(\d+) bytes', Mashigar_bayanai_Jeri)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                ma_ajiya_Daraja = Path(임시)
                baƙo_Fayil(na_ura_mai_kwakwalwa, 2, Girma, ma_ajiya_Daraja / 'FileDemo.class')
                sauka = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ma_ajiya_Daraja), 'FileDemo'], cwd=str(ma_ajiya_Daraja), universal_newlines=True)
                assert sauka == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', sauka
                assert (ma_ajiya_Daraja / 'java.txt').read_bytes() == b'A\xffB'
            gyaran_Daraja(na_ura_mai_kwakwalwa, 'FileDemo.java', tushe.replace('output.write(65);', 'output.close(); output.write(65);'))
            na_ura_mai_kwakwalwa.Umarni('javac FileDemo.java', ['Exit: 0'])
            na_ura_mai_kwakwalwa.Umarni('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            gyaran_Daraja(na_ura_mai_kwakwalwa, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            na_ura_mai_kwakwalwa.Umarni('javac FileDemo.java', ['Exit: 0'])
            na_ura_mai_kwakwalwa.Umarni('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            na_ura_mai_kwakwalwa.Umarni('run hello recovered', ['Exit: 0'])
            결과[종류] = na_ura_mai_kwakwalwa.logu_naɗa.decode('utf-8', 'replace')
        finally:
            na_ura_mai_kwakwalwa.Rufe()
        print('PASS:', 종류, '게스트 Java Fayil 생성/이어쓰기/bayit_Daraja/EOF/닫힘/Kasa_aiki_Daraja/OpenJDK 교차 gudanar_Umarni', flush=True)
    (위치 / 'build/자바파일시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    gudanar_Umarni()
