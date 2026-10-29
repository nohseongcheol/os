#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Gweithredu_gorchymyn import prosiect_gwraidd

def Gweithredu_2():
    mesur_data=prosiect_gwraidd/'build/verification/coding';mesur_data.mkdir(parents=True,exist_ok=True)
    dilysu_adrodd={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((prosiect_gwraidd/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(prosiect_gwraidd/'Offer/allgludo_SDK.py')])
        with tarfile.open(str(prosiect_gwraidd/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(mesur_data))
        개발꾸러미=mesur_data/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Enw in ('통신종단점만들기','BIND_ADDRESS','자료전문보내기','자료전문받기','agor_ffeil','파일자료읽기','ysgrifennu_ffeil_data'):
            assert ' T '+Enw+'\n' in 심볼목록, Enw
        (mesur_data/'korean-function-symbols.txt').write_text(심볼목록)
        dilysu_adrodd['checks'].append('real-korean-c-function-symbols')
        def Gweithredu_gorchymyn(Enw,LLWYBR,arg_ARAE,예상결과):
            data_safle=subprocess.run(['python3',str(prosiect_gwraidd/'Offer/Gweithredu_ffeil.py'),str(LLWYBR)]+arg_ARAE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (mesur_data/(Enw+'.log')).write_bytes(data_safle.stdout);assert data_safle.returncode==0,data_safle.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in data_safle.stdout,data_safle.stdout;dilysu_adrodd['checks'].append(Enw)
        for 뒷부분 in ('c','cpp'):
            실행파일=mesur_data/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            Gweithredu_gorchymyn('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=mesur_data/'ffrwd_VALUE.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/ffrwd_VALUE.c'),'-o',str(실행파일)])
        Gweithredu_gorchymyn('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        Gweithredu_gorchymyn('korean-python',prosiect_gwraidd/'예제/한글코딩/인사.py',['--include',str(prosiect_gwraidd/'예제/한글코딩/Cymraeg.py')],'안녕하세요 누리')
        Gweithredu_gorchymyn('guest-korean-javac',prosiect_gwraidd/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        dilysu_adrodd['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(mesur_data/'report.json').write_text(json.dumps(dilysu_adrodd,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Gweithredu_2()
