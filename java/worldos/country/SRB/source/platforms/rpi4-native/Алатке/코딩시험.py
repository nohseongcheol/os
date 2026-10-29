#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Изврши_команда import пројектовати_корен

def Покрени():
    мера_подаци=пројектовати_корен/'build/verification/coding';мера_подаци.mkdir(parents=True,exist_ok=True)
    провјера_извештај={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((пројектовати_корен/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(пројектовати_корен/'Алатке/개발꾸러미내보내기.py')])
        with tarfile.open(str(пројектовати_корен/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(мера_подаци))
        개발꾸러미=мера_подаци/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Назив in ('Направи_крајња_тачка','повезати_адреса','자료전문보내기','자료전문받기','креирати_фајл','파일자료읽기','писати_фајл_подаци'):
            assert ' T '+Назив+'\n' in 심볼목록, Назив
        (мера_подаци/'korean-function-symbols.txt').write_text(심볼목록)
        провјера_извештај['checks'].append('real-korean-c-function-symbols')
        def Изврши_команда(Назив,ПУТАЊА,аргумент_низ,예상결과):
            подаци_позиција=subprocess.run(['python3',str(пројектовати_корен/'Алатке/Изврши_фајл.py'),str(ПУТАЊА)]+аргумент_низ,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (мера_подаци/(Назив+'.log')).write_bytes(подаци_позиција.stdout);assert подаци_позиција.returncode==0,подаци_позиција.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in подаци_позиција.stdout,подаци_позиција.stdout;провјера_извештај['checks'].append(Назив)
        for 뒷부분 in ('c','cpp'):
            실행파일=мера_подаци/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            Изврши_команда('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=мера_подаци/'ток_вриједност.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/ток_вриједност.c'),'-o',str(실행파일)])
        Изврши_команда('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        Изврши_команда('korean-python',пројектовати_корен/'예제/한글코딩/인사.py',['--include',str(пројектовати_корен/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        Изврши_команда('guest-korean-javac',пројектовати_корен/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        провјера_извештај['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(мера_подаци/'report.json').write_text(json.dumps(провјера_извештај,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Покрени()
