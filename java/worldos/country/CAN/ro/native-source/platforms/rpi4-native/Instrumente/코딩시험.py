#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from executa_comandă import Project_rădăcină

def Pornește():
    KR_date=Project_rădăcină/'build/verification/coding';KR_date.mkdir(parents=True,exist_ok=True)
    validare_raport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rădăcină/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(Project_rădăcină/'Instrumente/exporta_SDK.py')])
        with tarfile.open(str(Project_rădăcină/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(KR_date))
        kit_de_dezvoltare=KR_date/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(kit_de_dezvoltare/'lib/libposix-kor-user.a')]).decode()
        for Nume in ('crea_participant','BIND_adresa','trimite_diagramă_informații_date','primi_diagramă_informații_date','crea_Fișier','파일자료읽기','scriere_Fișier_date'):
            assert ' T '+Nume+'\n' in 심볼목록, Nume
        (KR_date/'korean-function-symbols.txt').write_text(심볼목록)
        validare_raport['checks'].append('real-korean-c-function-symbols')
        def executa_comandă(Nume,Cale,argument_ARRAY,예상결과):
            date_poziție=subprocess.run(['python3',str(Project_rădăcină/'Instrumente/executa_Fișier.py'),str(Cale)]+argument_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (KR_date/(Nume+'.log')).write_bytes(date_poziție.stdout);assert date_poziție.returncode==0,date_poziție.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in date_poziție.stdout,date_poziție.stdout;validare_raport['checks'].append(Nume)
        for 뒷부분 in ('c','cpp'):
            실행파일=KR_date/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(kit_de_dezvoltare/'compile.py'),str(kit_de_dezvoltare/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            executa_comandă('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=KR_date/'flux_VALUE.elf'
        subprocess.check_call(['python3',str(kit_de_dezvoltare/'compile.py'),str(kit_de_dezvoltare/'examples/flux_VALUE.c'),'-o',str(실행파일)])
        executa_comandă('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        executa_comandă('korean-python',Project_rădăcină/'예제/한글코딩/인사.py',['--include',str(Project_rădăcină/'예제/한글코딩/Română.py')],'안녕하세요 누리')
        executa_comandă('guest-korean-javac',Project_rădăcină/'예제/한글코딩/인사.java',[],'안녕하세요 · total_VALUE=42')
        validare_raport['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(KR_date/'report.json').write_text(json.dumps(validare_raport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Pornește()
