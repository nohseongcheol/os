#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from phethagatša_taelo import 기준

def Diriša():
    결과자료=기준/'build/verification/coding';결과자료.mkdir(parents=True,exist_ok=True)
    tiišetšo_pego={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(기준/'Ditholosi/개발꾸러미내보내기.py')])
        with tarfile.open(str(기준/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(결과자료))
        개발꾸러미=결과자료/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Leina in ('통신종단점만들기','tlama_atrese','자료전문보내기','자료전문받기','bula_faele','파일자료읽기','ngwala_faele_data'):
            assert ' T '+Leina+'\n' in 심볼목록, Leina
        (결과자료/'korean-function-symbols.txt').write_text(심볼목록)
        tiišetšo_pego['checks'].append('real-korean-c-function-symbols')
        def phethagatša_taelo(Leina,Tsejana,akumente_arei,예상결과):
            자료위치=subprocess.run(['python3',str(기준/'Ditholosi/phethagatša_faele.py'),str(Tsejana)]+akumente_arei,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (결과자료/(Leina+'.log')).write_bytes(자료위치.stdout);assert 자료위치.returncode==0,자료위치.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in 자료위치.stdout,자료위치.stdout;tiišetšo_pego['checks'].append(Leina)
        for 뒷부분 in ('c','cpp'):
            실행파일=결과자료/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            phethagatša_taelo('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=결과자료/'Stream_boleng.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/Stream_boleng.c'),'-o',str(실행파일)])
        phethagatša_taelo('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        phethagatša_taelo('korean-python',기준/'예제/한글코딩/인사.py',['--include',str(기준/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        phethagatša_taelo('guest-korean-javac',기준/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        tiišetšo_pego['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(결과자료/'report.json').write_text(json.dumps(tiišetšo_pego,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Diriša()
