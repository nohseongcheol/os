#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from δοκιμή_χρήστης_δίκτυο import εικονική_μηχανή, Θέση
from 자바시험 import Τροποποίησε_τιμή, Επισκέπτης_Αρχείο

def εκτελώ_εντολή():
    μέτρηση = {}
    ΠΗΓΗ = (Θέση.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        υπολογιστής_5eb260fa = εικονική_μηχανή(Θέση / ('build/kernel.' + 종류), 종류, δίκτυο_τιμή=False)
        try:
            Τροποποίησε_τιμή(υπολογιστής_5eb260fa, 'FileDemo.java', ΠΗΓΗ)
            υπολογιστής_5eb260fa.Εντολή('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for επανάληψη_τιμή in range(2):
                Έξοδος = υπολογιστής_5eb260fa.Εντολή('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            καταχώρηση_Λίστα = υπολογιστής_5eb260fa.Εντολή('ls', ['java.txt  3 bytes'])
            Μέγεθος = int(re.search(r'FileDemo.class\s+(\d+) bytes', καταχώρηση_Λίστα)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                Κατάλογος_τιμή = Path(임시)
                Επισκέπτης_Αρχείο(υπολογιστής_5eb260fa, 2, Μέγεθος, Κατάλογος_τιμή / 'FileDemo.class')
                φιλοξενώ = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Κατάλογος_τιμή), 'FileDemo'], cwd=str(Κατάλογος_τιμή), universal_newlines=True)
                assert φιλοξενώ == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', φιλοξενώ
                assert (Κατάλογος_τιμή / 'java.txt').read_bytes() == b'A\xffB'
            Τροποποίησε_τιμή(υπολογιστής_5eb260fa, 'FileDemo.java', ΠΗΓΗ.replace('output.write(65);', 'output.close(); output.write(65);'))
            υπολογιστής_5eb260fa.Εντολή('javac FileDemo.java', ['Exit: 0'])
            υπολογιστής_5eb260fa.Εντολή('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            Τροποποίησε_τιμή(υπολογιστής_5eb260fa, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            υπολογιστής_5eb260fa.Εντολή('javac FileDemo.java', ['Exit: 0'])
            υπολογιστής_5eb260fa.Εντολή('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            υπολογιστής_5eb260fa.Εντολή('run hello recovered', ['Exit: 0'])
            μέτρηση[종류] = υπολογιστής_5eb260fa.καταγράφω_ρεκόρ.decode('utf-8', 'replace')
        finally:
            υπολογιστής_5eb260fa.Κλείσιμο()
        print('PASS:', 종류, '게스트 Java Αρχείο δημιουργώ/이어쓰기/바이트/EOF/πληροφοριακά_συστήματα_κλειστή/αποτυχία_τιμή/OpenJDK 교차 εκτελώ_εντολή', flush=True)
    (Θέση / 'build/자바파일시험.json').write_text(json.dumps(μέτρηση, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    εκτελώ_εντολή()
