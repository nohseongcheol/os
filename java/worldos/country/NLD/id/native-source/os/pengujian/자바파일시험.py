#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import mesin_virtual, posisi
from 자바시험 import Edit_VALUE, tamu_file

def Jalankan_perintah():
    hasil = {}
    kodeSumber = (posisi.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        mesin = mesin_virtual(posisi / ('build/kernel.' + 종류), 종류, jaringan_VALUE=False)
        try:
            Edit_VALUE(mesin, 'FileDemo.java', kodeSumber)
            mesin.perintah('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sprint_VALUE in range(2):
                keluaranTeks = mesin.perintah('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            entri_Daftar = mesin.perintah('ls', ['java.txt  3 bytes'])
            Ukuran = int(re.search(r'FileDemo.class\s+(\d+) bytes', entri_Daftar)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                Direktori_VALUE = Path(임시)
                tamu_file(mesin, 2, Ukuran, Direktori_VALUE / 'FileDemo.class')
                host = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Direktori_VALUE), 'FileDemo'], cwd=str(Direktori_VALUE), universal_newlines=True)
                assert host == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', host
                assert (Direktori_VALUE / 'java.txt').read_bytes() == b'A\xffB'
            Edit_VALUE(mesin, 'FileDemo.java', kodeSumber.replace('output.write(65);', 'output.close(); output.write(65);'))
            mesin.perintah('javac FileDemo.java', ['Exit: 0'])
            mesin.perintah('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            Edit_VALUE(mesin, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            mesin.perintah('javac FileDemo.java', ['Exit: 0'])
            mesin.perintah('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            mesin.perintah('run hello recovered', ['Exit: 0'])
            hasil[종류] = mesin.LOG_baris.decode('utf-8', 'replace')
        finally:
            mesin.Tutup()
        print('PASS:', 종류, '게스트 Java berkas buat/이어쓰기/byte_VALUE/EOF/닫힘/kegagalan_VALUE/OpenJDK 교차 Jalankan_perintah', flush=True)
    (posisi / 'build/자바파일시험.json').write_text(json.dumps(hasil, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Jalankan_perintah()
