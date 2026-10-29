#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from Utfør_kommando import spegle_rot

def Køyr_2():
    forretningsmål_data=spegle_rot/'build/verification/coding';forretningsmål_data.mkdir(parents=True,exist_ok=True)
    validering_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((spegle_rot/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(spegle_rot/'Verktøy/개발꾸러미내보내기.py')])
        with tarfile.open(str(spegle_rot/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 압축묶음:압축묶음.extractall(str(forretningsmål_data))
        개발꾸러미=forretningsmål_data/'jkoros-native-sdk'
        심볼목록=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(개발꾸러미/'lib/libposix-kor-user.a')]).decode()
        for Namn in ('Opprett_endepunkt','BIND_ADDRESS','자료전문보내기','자료전문받기','opne_fil','파일자료읽기','skrive_fil_data'):
            assert ' T '+Namn+'\n' in 심볼목록, Namn
        (forretningsmål_data/'korean-function-symbols.txt').write_text(심볼목록)
        validering_rapport['checks'].append('real-korean-c-function-symbols')
        def Utfør_kommando(Namn,STIGE,argument_ARRAY,예상결과):
            data_plassere=subprocess.run(['python3',str(spegle_rot/'Verktøy/Utfør_fil.py'),str(STIGE)]+argument_ARRAY,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (forretningsmål_data/(Namn+'.log')).write_bytes(data_plassere.stdout);assert data_plassere.returncode==0,data_plassere.stdout.decode('utf-8','replace')
            assert 예상결과.encode() in data_plassere.stdout,data_plassere.stdout;validering_rapport['checks'].append(Namn)
        for 뒷부분 in ('c','cpp'):
            실행파일=forretningsmål_data/('인사-'+뒷부분+'.elf')
            subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples'/('인사.'+뒷부분)),'-o',str(실행파일)])
            Utfør_kommando('korean-'+뒷부분,실행파일,[],'posix-kor 호출')
        실행파일=forretningsmål_data/'Stream_VALUE.elf'
        subprocess.check_call(['python3',str(개발꾸러미/'compile.py'),str(개발꾸러미/'examples/Stream_VALUE.c'),'-o',str(실행파일)])
        Utfør_kommando('c-stream-queues',실행파일,[],'C posix-kor 연결형 통신 PASS')
        Utfør_kommando('korean-python',spegle_rot/'예제/한글코딩/인사.py',['--include',str(spegle_rot/'예제/한글코딩/한국어.py')],'안녕하세요 누리')
        Utfør_kommando('guest-korean-javac',spegle_rot/'예제/한글코딩/인사.java',[],'안녕하세요 · 합계=42')
        validering_rapport['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(forretningsmål_data/'report.json').write_text(json.dumps(validering_rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Køyr_2()
