#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from keyra_skipun import verk_rót

def Keyra_2():
    mæld_stærð_gögn=verk_rót/'build/verification/coding';mæld_stærð_gögn.mkdir(parents=True,exist_ok=True)
    prófun_skrá={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((verk_rót/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(verk_rót/'Verkfæri/개발꾸러미내보내기.py')])
        with tarfile.open(str(verk_rót/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(mæld_stærð_gögn))
        개발꾸러미=mæld_stærð_gögn/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Heiti in ('stofna_endastöð','BIND_slóð','자료전문보내기','자료전문받기','opið_skrá','파일자료읽기','skrifa_skrá_gögn'):
            assert ' T '+Heiti+'\n' in 심볼목록, Heiti
        (mæld_stærð_gögn/'korean-function-symbols.txt').write_text(심볼목록)
        prófun_skrá['checks'].append('real-korean-c-function-symbols')
        def keyra_skipun(Heiti,SLÓÐ,frumbreyta_ARRAY,예상결과):
            gögn_staða=subprocess.run(['python3',str(verk_rót/'Verkfæri/keyra_skrá.py'),str(SLÓÐ)]+frumbreyta_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (mæld_stærð_gögn/(Heiti+'.log')).write_bytes(gögn_staða.stdout);assert gögn_staða.returncode==0,gögn_staða.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in gögn_staða.stdout,gögn_staða.stdout;prófun_skrá['checks'].append(Heiti)
        for 뒷부분 in ('c','cpp'):
            실행파일=mæld_stærð_gögn/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            keyra_skipun('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=mæld_stærð_gögn/'Stream_VALUE.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/Stream_VALUE.c'),'-o',str(실행파일)])
        keyra_skipun('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        keyra_skipun('korean-python',verk_rót/'예제/한글코딩/인사.py',['--include',str(verk_rót/'예제/한글코딩/Íslenska.py')],'안녕하세요 누리')
        keyra_skipun('guest-korean-javac',verk_rót/'예제/한글코딩/인사.java',[],'안녕하세요 · samtala_VALUE=42')
        prófun_skrá['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(mæld_stærð_gögn/'report.json').write_text(json.dumps(prófun_skrá,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Keyra_2()
