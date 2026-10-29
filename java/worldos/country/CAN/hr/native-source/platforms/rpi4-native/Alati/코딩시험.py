#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Izvrši_naredba import akcija_korijen

def Pokreni():
    KR_podaci=akcija_korijen/'build/verification/coding';KR_podaci.mkdir(parents=True,exist_ok=True)
    provjera_izvješće={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((akcija_korijen/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(akcija_korijen/'Alati/izvezi_SDK.py')])
        with tarfile.open(str(akcija_korijen/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(KR_podaci))
        set_razvojnih_alata=KR_podaci/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(set_razvojnih_alata/'lib/libposix-kor-user.a')]).decode()
        for Ime in ('Create_sudionik','BIND_adresa','slati_datogram_podaci','primiti_datogram_podaci','otvoreno_Datoteka','파일자료읽기','zapisivanje_Datoteka_podaci'):
            assert ' T '+Ime+'\n' in 심볼목록, Ime
        (KR_podaci/'korean-function-symbols.txt').write_text(심볼목록)
        provjera_izvješće['checks'].append('real-korean-c-function-symbols')
        def Izvrši_naredba(Ime,PUTANJA,argument_ARRAY,예상결과):
            podaci_položaj=subprocess.run(['python3',str(akcija_korijen/'Alati/Izvrši_Datoteka.py'),str(PUTANJA)]+argument_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (KR_podaci/(Ime+'.log')).write_bytes(podaci_položaj.stdout);assert podaci_položaj.returncode==0,podaci_položaj.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in podaci_položaj.stdout,podaci_položaj.stdout;provjera_izvješće['checks'].append(Ime)
        for 뒷부분 in ('c','cpp'):
            실행파일=KR_podaci/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(set_razvojnih_alata/'compile.py'),str(set_razvojnih_alata/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            Izvrši_naredba('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=KR_podaci/'tok_VALUE.elf'
        subprocess.check_call(['python3',str(set_razvojnih_alata/'compile.py'),str(set_razvojnih_alata/'examples/tok_VALUE.c'),'-o',str(실행파일)])
        Izvrši_naredba('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        Izvrši_naredba('korean-python',akcija_korijen/'예제/한글코딩/인사.py',['--include',str(akcija_korijen/'예제/한글코딩/hrvatski.py')],'안녕하세요 누리')
        Izvrši_naredba('guest-korean-javac',akcija_korijen/'예제/한글코딩/인사.java',[],'안녕하세요 · ukupni_zbroj_VALUE=42')
        provjera_izvješće['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(KR_podaci/'report.json').write_text(json.dumps(provjera_izvješće,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Pokreni()
