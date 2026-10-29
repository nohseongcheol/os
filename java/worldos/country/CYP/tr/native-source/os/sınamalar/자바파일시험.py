#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from test_kullanıcı_ağ import VM, konum
from 자바시험 import Düzenle_değer, konuk_Dosya

def yürütmek_komut():
    sonuç = {}
    kaynakKod = (konum.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for Tip_değer in ('elf', 'iso'):
        makine = VM(konum / ('build/kernel.' + Tip_değer), Tip_değer, ağ_değer=False)
        try:
            Düzenle_değer(makine, 'FileDemo.java', kaynakKod)
            makine.komut('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for öğe_değer_58902391 in range(2):
                metinÇıktısı = makine.komut('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            girdi_Liste = makine.komut('ls', ['java.txt  3 bytes'])
            Boyut = int(re.search(r'FileDemo.class\s+(\d+) bytes', girdi_Liste)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                dizin_değer = Path(임시)
                konuk_Dosya(makine, 2, Boyut, dizin_değer / 'FileDemo.class')
                konak = subprocess.check_output(['java', '-Xverify:all', '-cp', str(dizin_değer), 'FileDemo'], cwd=str(dizin_değer), universal_newlines=True)
                assert konak == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', konak
                assert (dizin_değer / 'java.txt').read_bytes() == b'A\xffB'
            Düzenle_değer(makine, 'FileDemo.java', kaynakKod.replace('output.write(65);', 'output.close(); output.write(65);'))
            makine.komut('javac FileDemo.java', ['Exit: 0'])
            makine.komut('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            Düzenle_değer(makine, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            makine.komut('javac FileDemo.java', ['Exit: 0'])
            makine.komut('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            makine.komut('run hello recovered', ['Exit: 0'])
            sonuç[Tip_değer] = makine.LOG_KAYIT.decode('utf-8', 'replace')
        finally:
            makine.Kapat()
        print('PASS:', Tip_değer, '게스트 Java dosya oluşturmak/이어쓰기/bayt_değer/EOF/bilgi_teknolojisi_kapalı/hata_değer/OpenJDK 교차 yürütmek_komut', flush=True)
    (konum / 'build/자바파일시험.json').write_text(json.dumps(sonuç, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    yürütmek_komut()
