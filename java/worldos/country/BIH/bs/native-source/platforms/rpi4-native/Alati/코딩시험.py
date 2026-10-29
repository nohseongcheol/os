#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Izvrši_komanda import projicirati_koijen

def Pokreni():
    mjera_podaci=projicirati_koijen/'build/verification/coding';mjera_podaci.mkdir(parents=True,exist_ok=True)
    provjera_izvještaj={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projicirati_koijen/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(projicirati_koijen/'Alati/izvesti_SDK.py')])
        with tarfile.open(str(projicirati_koijen/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(mjera_podaci))
        개발꾸러미=mjera_podaci/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Naziv in ('Create_završna_tačka','BIND_adresa','자료전문보내기','자료전문받기','kreirati_fajl','파일자료읽기','pisati_fajl_podaci'):
            assert ' T '+Naziv+'\n' in 심볼목록, Naziv
        (mjera_podaci/'korean-function-symbols.txt').write_text(심볼목록)
        provjera_izvještaj['checks'].append('real-korean-c-function-symbols')
        def Izvrši_komanda(Naziv,Putanja,argument_niz,예상결과):
            podaci_položaj=subprocess.run(['python3',str(projicirati_koijen/'Alati/Izvrši_fajl.py'),str(Putanja)]+argument_niz,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (mjera_podaci/(Naziv+'.log')).write_bytes(podaci_položaj.stdout);assert podaci_položaj.returncode==0,podaci_položaj.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in podaci_položaj.stdout,podaci_položaj.stdout;provjera_izvještaj['checks'].append(Naziv)
        for 뒷부분 in ('c','cpp'):
            실행파일=mjera_podaci/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            Izvrši_komanda('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=mjera_podaci/'tok_VALUE.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/tok_VALUE.c'),'-o',str(실행파일)])
        Izvrši_komanda('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        Izvrši_komanda('korean-python',projicirati_koijen/'예제/한글코딩/인사.py',['--include',str(projicirati_koijen/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        Izvrši_komanda('guest-korean-javac',projicirati_koijen/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        provjera_izvještaj['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(mjera_podaci/'report.json').write_text(json.dumps(provjera_izvještaj,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Pokreni()
