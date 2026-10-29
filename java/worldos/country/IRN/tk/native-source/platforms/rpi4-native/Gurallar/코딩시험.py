#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from ýerine_ýetir_buýruk import 기준

def Bitir():
    결과자료=기준/'build/verification/coding';결과자료.mkdir(parents=True,exist_ok=True)
    barlag_hasabat={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(기준/'Gurallar/개발꾸러미내보내기.py')])
        with tarfile.open(str(기준/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(결과자료))
        개발꾸러미=결과자료/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Ad in ('통신종단점만들기','BIND_salgy','자료전문보내기','자료전문받기','aç_faýl','파일자료읽기','ýaz_faýl_maglumat'):
            assert ' T '+Ad+'\n' in 심볼목록, Ad
        (결과자료/'korean-function-symbols.txt').write_text(심볼목록)
        barlag_hasabat['checks'].append('real-korean-c-function-symbols')
        def ýerine_ýetir_buýruk(Ad,Ýol,argument_ARRAY,예상결과):
            자료위치=subprocess.run(['python3',str(기준/'Gurallar/ýerine_ýetir_faýl.py'),str(Ýol)]+argument_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (결과자료/(Ad+'.log')).write_bytes(자료위치.stdout);assert 자료위치.returncode==0,자료위치.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in 자료위치.stdout,자료위치.stdout;barlag_hasabat['checks'].append(Ad)
        for 뒷부분 in ('c','cpp'):
            실행파일=결과자료/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            ýerine_ýetir_buýruk('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=결과자료/'Stream_baha.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/Stream_baha.c'),'-o',str(실행파일)])
        ýerine_ýetir_buýruk('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        ýerine_ýetir_buýruk('korean-python',기준/'예제/한글코딩/인사.py',['--include',str(기준/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        ýerine_ýetir_buýruk('guest-korean-javac',기준/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        barlag_hasabat['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(결과자료/'report.json').write_text(json.dumps(barlag_hasabat,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Bitir()
