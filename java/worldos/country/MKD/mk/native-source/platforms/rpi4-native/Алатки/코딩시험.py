#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Изврши_наредба import Project_корен

def Изврши_2():
    мерка_податоци=Project_корен/'build/verification/coding';мерка_податоци.mkdir(parents=True,exist_ok=True)
    проверка_извештај={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_корен/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(Project_корен/'Алатки/извези_SDK.py')])
        with tarfile.open(str(Project_корен/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(мерка_податоци))
        개발꾸러미=мерка_податоци/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Име in ('통신종단점만들기','БИНД_адреса','자료전문보내기','자료전문받기','отвори_датотека','파일자료읽기','запиши_датотека_податоци'):
            assert ' T '+Име+'\n' in 심볼목록, Име
        (мерка_податоци/'korean-function-symbols.txt').write_text(심볼목록)
        проверка_извештај['checks'].append('real-korean-c-function-symbols')
        def Изврши_наредба(Име,ПАТЕКА,аргумент_низа,예상결과):
            податоци_позиционирање=subprocess.run(['python3',str(Project_корен/'Алатки/Изврши_датотека.py'),str(ПАТЕКА)]+аргумент_низа,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (мерка_податоци/(Име+'.log')).write_bytes(податоци_позиционирање.stdout);assert податоци_позиционирање.returncode==0,податоци_позиционирање.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in податоци_позиционирање.stdout,податоци_позиционирање.stdout;проверка_извештај['checks'].append(Име)
        for 뒷부분 in ('c','cpp'):
            실행파일=мерка_податоци/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            Изврши_наредба('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=мерка_податоци/'Stream_VALUE.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/Stream_VALUE.c'),'-o',str(실행파일)])
        Изврши_наредба('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        Изврши_наредба('korean-python',Project_корен/'예제/한글코딩/인사.py',['--include',str(Project_корен/'예제/한글코딩/Македонски.py')],'안녕하세요 누리')
        Изврши_наредба('guest-korean-javac',Project_корен/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        проверка_извештај['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(мерка_податоци/'report.json').write_text(json.dumps(проверка_извештај,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Изврши_2()
