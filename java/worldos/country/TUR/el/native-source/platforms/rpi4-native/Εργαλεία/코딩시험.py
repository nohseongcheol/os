#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from εκτελώ_εντολή import έργο_ρίζα

def Εκτέλεση_2():
    μέτρηση_δεδομένα=έργο_ρίζα/'build/verification/coding';μέτρηση_δεδομένα.mkdir(parents=True,exist_ok=True)
    επικύρωση_έκθεση={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((έργο_ρίζα/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(έργο_ρίζα/'Εργαλεία/개발꾸러미내보내기.py')])
        with tarfile.open(str(έργο_ρίζα/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(μέτρηση_δεδομένα))
        κιτ_ανάπτυξης_λογισμικού=μέτρηση_δεδομένα/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(κιτ_ανάπτυξης_λογισμικού/'lib/libposix-kor-user.a')]).decode()
        for Όνομα in ('ανοίγω_τελικό_σημείο','συνδέω_διεύθυνση','στέλνω_αυτοδύναμο_πακέτο_δεδομένα','λαμβάνω_αυτοδύναμο_πακέτο_δεδομένα','ανοίγω_Αρχείο','파일자료읽기','εγγράφω_Αρχείο_δεδομένα'):
            assert ' T '+Όνομα+'\n' in 심볼목록, Όνομα
        (μέτρηση_δεδομένα/'korean-function-symbols.txt').write_text(심볼목록)
        επικύρωση_έκθεση['checks'].append('real-korean-c-function-symbols')
        def εκτελώ_εντολή(Όνομα,ΔΙΑΔΡΟΜΗ,όρισμα_πίνακας,예상결과):
            δεδομένα_θέση=subprocess.run(['python3',str(έργο_ρίζα/'Εργαλεία/εκτελώ_Αρχείο.py'),str(ΔΙΑΔΡΟΜΗ)]+όρισμα_πίνακας,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (μέτρηση_δεδομένα/(Όνομα+'.log')).write_bytes(δεδομένα_θέση.stdout);assert δεδομένα_θέση.returncode==0,δεδομένα_θέση.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in δεδομένα_θέση.stdout,δεδομένα_θέση.stdout;επικύρωση_έκθεση['checks'].append(Όνομα)
        for 뒷부분 in ('c','cpp'):
            εκτελέσιμο=μέτρηση_δεδομένα/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(κιτ_ανάπτυξης_λογισμικού/'compile.py'),str(κιτ_ανάπτυξης_λογισμικού/'examples'/('인사.'+뒷부분)),'-o',str(εκτελέσιμο)])
            εκτελώ_εντολή('korean-'+뒷부분,εκτελέσιμο,[],'posix-kor 호출')
        εκτελέσιμο=μέτρηση_δεδομένα/'ροή_τιμή.elf'
        subprocess.check_call(['python3',str(κιτ_ανάπτυξης_λογισμικού/'compile.py'),str(κιτ_ανάπτυξης_λογισμικού/'examples/ροή_τιμή.c'),'-o',str(εκτελέσιμο)])
        εκτελώ_εντολή('c-stream-queues',εκτελέσιμο,[],'C posix-kor 연결형 통신 PASS')
        εκτελώ_εντολή('korean-python',έργο_ρίζα/'예제/한글코딩/인사.py',['--include',str(έργο_ρίζα/'예제/한글코딩/ελληνικά.py')],'안녕하세요 누리')
        εκτελώ_εντολή('guest-korean-javac',έργο_ρίζα/'예제/한글코딩/인사.java',[],'안녕하세요 · σύνολο_τιμή=42')
        επικύρωση_έκθεση['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(μέτρηση_δεδομένα/'report.json').write_text(json.dumps(επικύρωση_έκθεση,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Εκτέλεση_2()
