#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Izpildīt_komanda import Project_sakne

def Palaist():
    mērs_dati=Project_sakne/'build/verification/coding';mērs_dati.mkdir(parents=True,exist_ok=True)
    validācija_ziņot={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_sakne/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(Project_sakne/'Rīki/eksportēt_SDK.py')])
        with tarfile.open(str(Project_sakne/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(mērs_dati))
        programmizstrādes_komplekts=mērs_dati/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(programmizstrādes_komplekts/'lib/libposix-kor-user.a')]).decode()
        for Nosaukums in ('atvērt_dalībnieks','BIND_adrese','sūtīt_datogramma_dati','saņemt_datogramma_dati','atvērt_Fails','파일자료읽기','rakstīšana_Fails_dati'):
            assert ' T '+Nosaukums+'\n' in 심볼목록, Nosaukums
        (mērs_dati/'korean-function-symbols.txt').write_text(심볼목록)
        validācija_ziņot['checks'].append('real-korean-c-function-symbols')
        def Izpildīt_komanda(Nosaukums,CEĻŠ,arg_ARRAY,예상결과):
            dati_amats=subprocess.run(['python3',str(Project_sakne/'Rīki/Izpildīt_Fails.py'),str(CEĻŠ)]+arg_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (mērs_dati/(Nosaukums+'.log')).write_bytes(dati_amats.stdout);assert dati_amats.returncode==0,dati_amats.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in dati_amats.stdout,dati_amats.stdout;validācija_ziņot['checks'].append(Nosaukums)
        for 뒷부분 in ('c','cpp'):
            izpildāms_fails=mērs_dati/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(programmizstrādes_komplekts/'compile.py'),str(programmizstrādes_komplekts/'examples'/('인사.'+뒷부분)),'-o',str(izpildāms_fails)])
            Izpildīt_komanda('korean-'+뒷부분,izpildāms_fails,[],'posix-kor 호출')
        izpildāms_fails=mērs_dati/'Stream_VALUE.elf'
        subprocess.check_call(['python3',str(programmizstrādes_komplekts/'compile.py'),str(programmizstrādes_komplekts/'examples/Stream_VALUE.c'),'-o',str(izpildāms_fails)])
        Izpildīt_komanda('c-stream-queues',izpildāms_fails,[],'C posix-kor 연결형 통신 PASS')
        Izpildīt_komanda('korean-python',Project_sakne/'예제/한글코딩/인사.py',['--include',str(Project_sakne/'예제/한글코딩/Latviešu.py')],'안녕하세요 누리')
        Izpildīt_komanda('guest-korean-javac',Project_sakne/'예제/한글코딩/인사.java',[],'안녕하세요 · kopsumma_VALUE=42')
        validācija_ziņot['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(mērs_dati/'report.json').write_text(json.dumps(validācija_ziņot,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Palaist()
