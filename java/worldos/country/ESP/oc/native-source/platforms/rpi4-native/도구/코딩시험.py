#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from 실행 import 기준

def Executar_2():
    결과자료=기준/'build/verification/coding';결과자료.mkdir(parents=True,exist_ok=True)
    검증기록={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(기준/'도구/개발꾸러미내보내기.py')])
        with tarfile.open(str(기준/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(결과자료))
        개발꾸러미=결과자료/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Nom in ('통신종단점만들기','통신주소묶기','자료전문보내기','자료전문받기','파일열기','파일자료읽기','파일자료쓰기'):
            assert ' T '+Nom+'\n' in 심볼목록, Nom
        (결과자료/'korean-function-symbols.txt').write_text(심볼목록)
        검증기록['checks'].append('real-korean-c-function-symbols')
        def 실행(Nom,CAMIN,인수배열,예상결과):
            자료위치=subprocess.run(['python3',str(기준/'도구/파일실행.py'),str(CAMIN)]+인수배열,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (결과자료/(Nom+'.log')).write_bytes(자료위치.stdout);assert 자료위치.returncode==0,자료위치.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in 자료위치.stdout,자료위치.stdout;검증기록['checks'].append(Nom)
        for 뒷부분 in ('c','cpp'):
            실행파일=결과자료/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            실행('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=결과자료/'흐름.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/흐름.c'),'-o',str(실행파일)])
        실행('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        실행('korean-python',기준/'예제/한글코딩/인사.py',['--include',str(기준/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        실행('guest-korean-javac',기준/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        검증기록['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(결과자료/'report.json').write_text(json.dumps(검증기록,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Executar_2()
