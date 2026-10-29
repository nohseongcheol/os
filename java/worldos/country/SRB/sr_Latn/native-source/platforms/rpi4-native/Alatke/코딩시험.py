#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Izvrši_komanda import radnja_koren

def koristiti():
    KR_podaci=radnja_koren/'build/verification/coding';KR_podaci.mkdir(parents=True,exist_ok=True)
    provera_valjanosti_izveštaj={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((radnja_koren/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(radnja_koren/'Alatke/izvesti_SDK.py')])
        with tarfile.open(str(radnja_koren/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(KR_podaci))
        komplet_za_razvoj_programa=KR_podaci/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(komplet_za_razvoj_programa/'lib/libposix-kor-user.a')]).decode()
        for ime in ('Create_učesnik','povezati_adresa','poslati_datagram_podaci','primiti_datagram_podaci','otvoren_Datoteka','파일자료읽기','파일자료쓰기'):
            assert ' T '+ime+'\n' in 심볼목록, ime
        (KR_podaci/'korean-function-symbols.txt').write_text(심볼목록)
        provera_valjanosti_izveštaj['checks'].append('real-korean-c-function-symbols')
        def Izvrši_komanda(ime,putanja,argument_niz,예상결과):
            podaci_pozicija=subprocess.run(['python3',str(radnja_koren/'Alatke/Izvrši_Datoteka.py'),str(putanja)]+argument_niz,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (KR_podaci/(ime+'.log')).write_bytes(podaci_pozicija.stdout);assert podaci_pozicija.returncode==0,podaci_pozicija.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in podaci_pozicija.stdout,podaci_pozicija.stdout;provera_valjanosti_izveštaj['checks'].append(ime)
        for 뒷부분 in ('c','cpp'):
            실행파일=KR_podaci/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(komplet_za_razvoj_programa/'compile.py'),str(komplet_za_razvoj_programa/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            Izvrši_komanda('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=KR_podaci/'tok_VALUE.elf'
        subprocess.check_call(['python3',str(komplet_za_razvoj_programa/'compile.py'),str(komplet_za_razvoj_programa/'examples/tok_VALUE.c'),'-o',str(실행파일)])
        Izvrši_komanda('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        Izvrši_komanda('korean-python',radnja_koren/'예제/한글코딩/인사.py',['--include',str(radnja_koren/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        Izvrši_komanda('guest-korean-javac',radnja_koren/'예제/한글코딩/인사.java',[],'안녕하세요 · ukupan_VALUE=42')
        provera_valjanosti_izveštaj['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(KR_podaci/'report.json').write_text(json.dumps(provera_valjanosti_izveštaj,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':koristiti()
