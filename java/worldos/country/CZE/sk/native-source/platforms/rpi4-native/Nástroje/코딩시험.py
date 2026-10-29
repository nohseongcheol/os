#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Vykonať_príkaz import akcia_koreň

def Spustiť_2():
    KR_údaje=akcia_koreň/'build/verification/coding';KR_údaje.mkdir(parents=True,exist_ok=True)
    overenie_správa={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((akcia_koreň/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(akcia_koreň/'Nástroje/exportovať_SDK.py')])
        with tarfile.open(str(akcia_koreň/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(KR_údaje))
        Development_Kit=KR_údaje/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(Development_Kit/'lib/libposix-kor-user.a')]).decode()
        for Názov in ('Create_účastník','BIND_adresa','odoslať_datagram_údaje','dostať_datagram_údaje','otvoriť_Súbor','파일자료읽기','zapísať_Súbor_údaje'):
            assert ' T '+Názov+'\n' in 심볼목록, Názov
        (KR_údaje/'korean-function-symbols.txt').write_text(심볼목록)
        overenie_správa['checks'].append('real-korean-c-function-symbols')
        def Vykonať_príkaz(Názov,Cesta,argument_pole,예상결과):
            údaje_pozícia=subprocess.run(['python3',str(akcia_koreň/'Nástroje/Vykonať_Súbor.py'),str(Cesta)]+argument_pole,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (KR_údaje/(Názov+'.log')).write_bytes(údaje_pozícia.stdout);assert údaje_pozícia.returncode==0,údaje_pozícia.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in údaje_pozícia.stdout,údaje_pozícia.stdout;overenie_správa['checks'].append(Názov)
        for 뒷부분 in ('c','cpp'):
            spustiteľný_súbor=KR_údaje/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(Development_Kit/'compile.py'),str(Development_Kit/'examples'/('인사.'+뒷부분)),'-o',str(spustiteľný_súbor)])
            Vykonať_príkaz('korean-'+뒷부분,spustiteľný_súbor,[],'posix-kor 호출')
        spustiteľný_súbor=KR_údaje/'Stream_VALUE.elf'
        subprocess.check_call(['python3',str(Development_Kit/'compile.py'),str(Development_Kit/'examples/Stream_VALUE.c'),'-o',str(spustiteľný_súbor)])
        Vykonať_príkaz('c-stream-queues',spustiteľný_súbor,[],'C posix-kor 연결형 통신 PASS')
        Vykonať_príkaz('korean-python',akcia_koreň/'예제/한글코딩/인사.py',['--include',str(akcia_koreň/'예제/한글코딩/Slovenský.py')],'안녕하세요 누리')
        Vykonať_príkaz('guest-korean-javac',akcia_koreň/'예제/한글코딩/인사.java',[],'안녕하세요 · celkovo_VALUE=42')
        overenie_správa['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(KR_údaje/'report.json').write_text(json.dumps(overenie_správa,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Spustiť_2()
